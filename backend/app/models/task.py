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
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Time Tracking
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    actual_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Scheduling
    assigned_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, 
        comment="When this task was scheduled to be worked on"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship()
    topic: Mapped["Topic"] = relationship()
    subtasks: Mapped[list["Subtask"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="Subtask.order",
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, user_id={self.user_id}, topic_id={self.topic_id}, status={self.status})>"


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
