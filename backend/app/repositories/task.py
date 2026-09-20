"""
Task repository.

Data access layer for Tasks, Subtasks, and TaskDependencies.
"""

from datetime import datetime, timezone
import logging

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task import Task, Subtask, TaskDependency, TaskStatus
from app.models.curriculum import Topic, LearningObjective

logger = logging.getLogger(__name__)


async def get_task_by_id(db: AsyncSession, task_id: int) -> Task | None:
    """Fetch a task by ID, eager loading subtasks, topic, and dependencies."""
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(
            selectinload(Task.topic),
            selectinload(Task.subtasks).selectinload(Subtask.learning_objective),
            selectinload(Task.dependencies).selectinload(TaskDependency.prerequisite_task),
        )
    )
    task = result.scalar_one_or_none()
    if task:
        task.prerequisite_task_ids = [dep.prerequisite_task_id for dep in getattr(task, "dependencies", [])]
    return task


async def get_user_tasks_for_day(db: AsyncSession, user_id: int, date: datetime) -> list[Task]:
    """Fetch a user's tasks scheduled for a specific date."""
    # Strip time part for comparison
    target_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)

    result = await db.execute(
        select(Task)
        .where(
            and_(
                Task.user_id == user_id,
                Task.assigned_date >= target_date,
                Task.assigned_date <= end_date
            )
        )
        .options(
            selectinload(Task.topic),
            selectinload(Task.subtasks).selectinload(Subtask.learning_objective),
            selectinload(Task.dependencies).selectinload(TaskDependency.prerequisite_task),
        )
    )
    tasks = list(result.scalars().all())
    for t in tasks:
        t.prerequisite_task_ids = [dep.prerequisite_task_id for dep in getattr(t, "dependencies", [])]
    return tasks


async def generate_tasks_for_day(db: AsyncSession, user_id: int, day_number: int, date: datetime) -> list[Task]:
    """
    Generate user tasks based on the curriculum day_number.
    Idempotent: won't duplicate tasks if they already exist for the user and topic.
    """
    logger.info("Generating tasks for user %s, day %s", user_id, day_number)
    
    # 1. Fetch topics for the day
    topics_result = await db.execute(
        select(Topic)
        .where(Topic.day_number == day_number, Topic.is_active.is_(True))
        .options(selectinload(Topic.objectives))
    )
    topics = topics_result.scalars().all()
    
    generated_tasks = []
    
    for topic in topics:
        # Check if task already exists
        existing = await db.execute(
            select(Task).where(and_(Task.user_id == user_id, Task.topic_id == topic.id))
        )
        task = existing.scalar_one_or_none()
        
        if not task:
            # Create Task
            task = Task(
                user_id=user_id,
                topic_id=topic.id,
                status=TaskStatus.TODO,
                estimated_hours=topic.estimated_hours,
                assigned_date=date,
            )
            db.add(task)
            await db.flush()  # To get task.id
            
            # Create Subtasks for LearningObjectives
            for obj in topic.objectives:
                subtask = Subtask(
                    task_id=task.id,
                    learning_objective_id=obj.id,
                    status=TaskStatus.TODO,
                    order=obj.order,
                )
                db.add(subtask)
            
            logger.info("Created Task %s for Topic %s", task.id, topic.id)
            generated_tasks.append(task)
            
    await db.flush()
    
    # Return all tasks for the day by querying again to load relationships
    return await get_user_tasks_for_day(db, user_id, date)


async def update_task(db: AsyncSession, task: Task, update_data: dict) -> Task:
    """Update task fields with dependency enforcement."""
    new_status = update_data.get("status")
    override = update_data.pop("override_dependencies", False)

    if new_status == TaskStatus.COMPLETED and not override:
        deps_result = await db.execute(
            select(TaskDependency)
            .where(TaskDependency.task_id == task.id)
            .options(selectinload(TaskDependency.prerequisite_task))
        )
        deps = deps_result.scalars().all()
        incomplete_deps = [
            d.prerequisite_task_id for d in deps
            if d.prerequisite_task and d.prerequisite_task.status != TaskStatus.COMPLETED
        ]
        if incomplete_deps:
            raise ValueError(
                f"Cannot complete task {task.id}: prerequisite task(s) {incomplete_deps} are not completed. "
                "Set override_dependencies=True to bypass."
            )

    for key, value in update_data.items():
        if hasattr(task, key):
            setattr(task, key, value)
            
    if new_status == TaskStatus.COMPLETED and not task.completed_at:
        task.completed_at = datetime.now(timezone.utc)
    elif new_status and new_status != TaskStatus.COMPLETED and task.completed_at:
        task.completed_at = None

    await db.flush()
    if not hasattr(task, "prerequisite_task_ids"):
        task.prerequisite_task_ids = [dep.prerequisite_task_id for dep in getattr(task, "dependencies", [])]
    return task


async def add_task_dependency(db: AsyncSession, task_id: int, prerequisite_task_id: int) -> TaskDependency:
    """Add a prerequisite dependency to a task."""
    if task_id == prerequisite_task_id:
        raise ValueError("A task cannot depend on itself.")

    existing = await db.execute(
        select(TaskDependency).where(
            and_(
                TaskDependency.task_id == task_id,
                TaskDependency.prerequisite_task_id == prerequisite_task_id,
            )
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError(f"Dependency already exists: task {task_id} already depends on {prerequisite_task_id}")

    dep = TaskDependency(task_id=task_id, prerequisite_task_id=prerequisite_task_id)
    db.add(dep)
    await db.flush()
    return dep


async def get_task_dependencies(db: AsyncSession, task_id: int) -> list[TaskDependency]:
    """List prerequisite dependencies for a task."""
    result = await db.execute(
        select(TaskDependency).where(TaskDependency.task_id == task_id)
    )
    return list(result.scalars().all())


async def remove_task_dependency(db: AsyncSession, task_id: int, prerequisite_task_id: int) -> bool:
    """Remove a prerequisite dependency."""
    result = await db.execute(
        select(TaskDependency).where(
            and_(
                TaskDependency.task_id == task_id,
                TaskDependency.prerequisite_task_id == prerequisite_task_id,
            )
        )
    )
    dep = result.scalar_one_or_none()
    if dep:
        await db.delete(dep)
        await db.flush()
        return True
    return False


async def get_subtask_by_id(db: AsyncSession, subtask_id: int) -> Subtask | None:
    """Fetch a subtask by ID."""
    result = await db.execute(
        select(Subtask)
        .where(Subtask.id == subtask_id)
        .options(selectinload(Subtask.learning_objective))
    )
    return result.scalar_one_or_none()


async def update_subtask(db: AsyncSession, subtask: Subtask, update_data: dict) -> Subtask:
    """Update subtask fields."""
    for key, value in update_data.items():
        if hasattr(subtask, key):
            setattr(subtask, key, value)
    await db.flush()
    return subtask

