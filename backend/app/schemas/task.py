"""
Task schemas.

Pydantic models for request/response validation in task endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.models.task import TaskStatus
from app.schemas.curriculum import TopicBrief, LearningObjectiveResponse


# ── Subtask ──────────────────────────────────────────────────────

class SubtaskBase(BaseModel):
    status: TaskStatus = TaskStatus.TODO
    notes: str | None = None


class SubtaskUpdate(SubtaskBase):
    pass


class SubtaskResponse(SubtaskBase):
    id: int
    task_id: int
    learning_objective_id: int
    order: int
    learning_objective: LearningObjectiveResponse

    model_config = {"from_attributes": True}


# ── Task ─────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    status: TaskStatus = TaskStatus.TODO
    notes: str | None = None
    actual_hours: float = 0.0


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    user_id: int
    topic_id: int
    estimated_hours: float
    assigned_date: datetime | None = None
    completed_at: datetime | None = None
    topic: TopicBrief
    subtasks: list[SubtaskResponse] = []

    model_config = {"from_attributes": True}


# ── Task Generation ──────────────────────────────────────────────

class TaskGenerationRequest(BaseModel):
    day_number: int = Field(ge=1, le=365, description="Day number in the 196-day plan")
