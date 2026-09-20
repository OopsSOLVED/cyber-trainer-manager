"""
Task schemas.

Pydantic models for request/response validation in task endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.models.task import TaskStatus, TaskPriority, TaskType
from app.schemas.curriculum import TopicBrief, LearningObjectiveResponse


# ── Subtask ──────────────────────────────────────────────────────

class SubtaskBase(BaseModel):
    status: TaskStatus = TaskStatus.TODO
    notes: str | None = None


class SubtaskUpdate(BaseModel):
    status: TaskStatus | None = None
    notes: str | None = None


class SubtaskResponse(SubtaskBase):
    id: int
    task_id: int
    learning_objective_id: int
    order: int
    learning_objective: LearningObjectiveResponse

    model_config = {"from_attributes": True}


# ── Task Dependency ──────────────────────────────────────────────

class TaskDependencyCreate(BaseModel):
    prerequisite_task_id: int = Field(..., description="ID of the prerequisite task that must be completed first")


class TaskDependencyResponse(BaseModel):
    id: int
    task_id: int
    prerequisite_task_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Task ─────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    task_type: TaskType = TaskType.STUDY
    notes: str | None = None
    actual_hours: float = 0.0
    due_date: datetime | None = None
    confidence_score: int | None = Field(default=None, ge=0, le=100, description="Confidence score from 0 to 100")
    review_date: datetime | None = None


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    task_type: TaskType | None = None
    notes: str | None = None
    actual_hours: float | None = None
    due_date: datetime | None = None
    confidence_score: int | None = Field(default=None, ge=0, le=100)
    review_date: datetime | None = None
    override_dependencies: bool = Field(default=False, description="Allow completing task even if prerequisites are incomplete")


class TaskResponse(TaskBase):
    id: int
    user_id: int
    topic_id: int
    estimated_hours: float
    assigned_date: datetime | None = None
    completed_at: datetime | None = None
    topic: TopicBrief
    subtasks: list[SubtaskResponse] = []
    prerequisite_task_ids: list[int] = []

    model_config = {"from_attributes": True}


# ── Task Generation ──────────────────────────────────────────────

class TaskGenerationRequest(BaseModel):
    day_number: int = Field(ge=1, le=365, description="Day number in the 196-day plan")

