"""
Task endpoints.

Handles CRUD operations for tasks and subtasks for the authenticated user,
as well as generation of daily tasks based on the curriculum.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.task import (
    TaskResponse,
    TaskUpdate,
    TaskGenerationRequest,
    SubtaskResponse,
    SubtaskUpdate,
    TaskDependencyCreate,
    TaskDependencyResponse,
)
from app.repositories.task import (
    get_user_tasks_for_day,
    generate_tasks_for_day,
    get_task_by_id,
    update_task,
    get_subtask_by_id,
    update_subtask,
    add_task_dependency,
    get_task_dependencies,
    remove_task_dependency,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/generate",
    response_model=list[TaskResponse],
    summary="Generate tasks for a curriculum day",
    description="Generates actionable tasks for the current user based on a specific day in the 196-day curriculum plan.",
)
async def generate_tasks(
    request: TaskGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate tasks for the user based on the specified curriculum day.
    Assigns the tasks to today's date. Idempotent.
    """
    today = datetime.now(timezone.utc)
    tasks = await generate_tasks_for_day(db, current_user.id, request.day_number, today)
    return tasks


@router.get(
    "/today",
    response_model=list[TaskResponse],
    summary="Get today's tasks",
    description="Returns all tasks assigned to the current user for today.",
)
async def get_today_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Fetch tasks for the current user assigned to today."""
    today = datetime.now(timezone.utc)
    tasks = await get_user_tasks_for_day(db, current_user.id, today)
    return tasks


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Updates task status, notes, priority, task_type, or hours. Validates prerequisites before completion.",
)
async def update_task_endpoint(
    task_id: int,
    update_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a task's status or details with dependency enforcement."""
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    try:
        updated = await update_task(db, task, update_data.model_dump(exclude_unset=True))
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{task_id}/dependencies",
    response_model=TaskDependencyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a task prerequisite dependency",
    description="Declares that task_id depends on prerequisite_task_id being completed first.",
)
async def add_dependency_endpoint(
    task_id: int,
    dependency_data: TaskDependencyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a prerequisite dependency to a task."""
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    prereq_task = await get_task_by_id(db, dependency_data.prerequisite_task_id)
    if not prereq_task:
        raise HTTPException(status_code=404, detail="Prerequisite task not found")
    if prereq_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Prerequisite task belongs to a different user")

    try:
        dep = await add_task_dependency(db, task_id, dependency_data.prerequisite_task_id)
        return dep
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{task_id}/dependencies",
    response_model=list[TaskDependencyResponse],
    summary="List task dependencies",
    description="Returns all prerequisite dependencies for the specified task.",
)
async def list_dependencies_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List dependencies for a task."""
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    return await get_task_dependencies(db, task_id)


@router.delete(
    "/{task_id}/dependencies/{prerequisite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a task prerequisite dependency",
)
async def remove_dependency_endpoint(
    task_id: int,
    prerequisite_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove a prerequisite dependency from a task."""
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    removed = await remove_task_dependency(db, task_id, prerequisite_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return None


@router.patch(
    "/subtasks/{subtask_id}",
    response_model=SubtaskResponse,
    summary="Update a subtask",
    description="Updates subtask status or notes.",
)
async def update_subtask_endpoint(
    subtask_id: int,
    update_data: SubtaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a subtask's status or notes."""
    subtask = await get_subtask_by_id(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
        
    # Check if the parent task belongs to the user
    task = await get_task_by_id(db, subtask.task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this subtask")
        
    updated = await update_subtask(db, subtask, update_data.model_dump(exclude_unset=True))
    return updated

