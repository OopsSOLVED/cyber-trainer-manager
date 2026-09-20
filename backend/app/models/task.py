"""
Task ORM models.

Defines the execution layer where the curriculum becomes actionable for users.
- Task: Represents a Topic assigned to a User.
- Subtask: Represents a LearningObjective assigned to a User under a Task.
"""

from enum import Enum as PyEnum
from sqlalchemy import String, Integer, Text, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.models.base import Base


class TaskStatus(str, PyEnum):
    """Status lifecycle of a task or subtask."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    NEEDS_REVIEW = "needs_review"


class TaskPriority(str, PyEnum):
    """Priority levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, PyEnum):
    """Types of tasks in the cybersecurity trainer curriculum."""
    STUDY = "study"
    PRACTICE = "practice"
    LAB = "lab"
    CTF = "ctf"
    READING = "reading"
    QUIZ = "quiz"
    REVIEW = "review"
    EXPLAIN = "explain"
    TEACH = "teach"
    PROJECT = "project"
    ASSESSMENT = "assessment"
    TROUBLESHOOTING = "troubleshooting"


class Task(Base):
    """
    A curriculum Topic assigned to a User for execution.
    """
    __tablename__ = "tasks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status", create_constraint=True),
        default=TaskStatus.TODO,
        nullable=False,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        String(20),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    task_type: Mapped[TaskType] = mapped_column(
        String(30),
        default=TaskType.STUDY,
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Time Tracking
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    actual_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Scheduling & Deadlines
    assigned_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, 
        comment="When this task was scheduled to be worked on"
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Due date for task completion"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Assessment & Review
    confidence_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Confidence score 0-100"
    )
    review_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Scheduled review date for spaced repetition"
    )

    # Relationships
    user: Mapped["User"] = relationship()
    topic: Mapped["Topic"] = relationship()
    subtasks: Mapped[list["Subtask"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="Subtask.order",
    )
    dependencies: Mapped[list["TaskDependency"]] = relationship(
        foreign_keys="[TaskDependency.task_id]",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    dependents: Mapped[list["TaskDependency"]] = relationship(
        foreign_keys="[TaskDependency.prerequisite_task_id]",
        back_populates="prerequisite_task",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, user_id={self.user_id}, topic_id={self.topic_id}, status={self.status})>"


class TaskDependency(Base):
    """
    Task prerequisite dependency relationship.
    A task cannot be completed if prerequisite tasks are not completed (unless overridden).
    """
    __tablename__ = "task_dependencies"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    prerequisite_task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    task: Mapped["Task"] = relationship(
        foreign_keys=[task_id],
        back_populates="dependencies",
    )
    prerequisite_task: Mapped["Task"] = relationship(
        foreign_keys=[prerequisite_task_id],
        back_populates="dependents",
    )

    def __repr__(self) -> str:
        return f"<TaskDependency(task_id={self.task_id}, prerequisite_task_id={self.prerequisite_task_id})>"


class Subtask(Base):
    """
    A curriculum LearningObjective assigned to a User under a Task.
    """
    __tablename__ = "subtasks"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    learning_objective_id: Mapped[int] = mapped_column(
        ForeignKey("learning_objectives.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status", create_constraint=True),
        default=TaskStatus.TODO,
        nullable=False,
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    task: Mapped["Task"] = relationship(back_populates="subtasks")
    learning_objective: Mapped["LearningObjective"] = relationship()

    def __repr__(self) -> str:
        return f"<Subtask(id={self.id}, task_id={self.task_id}, status={self.status})>"

