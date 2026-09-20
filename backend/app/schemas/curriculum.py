"""
Curriculum schemas.

Pydantic models for request/response validation in curriculum endpoints.
Supports the hierarchical structure: Phase → SkillLayer → Domain → Topic → Objective.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ── Learning Objective ───────────────────────────────────────────

class LearningObjectiveResponse(BaseModel):
    """Single learning objective."""
    id: int
    description: str
    order: int
    is_measurable: bool

    model_config = {"from_attributes": True}


# ── Topic ────────────────────────────────────────────────────────

class TopicBrief(BaseModel):
    """Topic without nested objectives (for list views)."""
    id: int
    name: str
    description: str | None = None
    order: int
    day_number: int | None = None
    estimated_hours: float
    difficulty: str

    model_config = {"from_attributes": True}


class TopicDetail(TopicBrief):
    """Topic with nested learning objectives."""
    objectives: list[LearningObjectiveResponse] = []


# ── Domain ───────────────────────────────────────────────────────

class DomainBrief(BaseModel):
    """Domain without nested topics."""
    id: int
    name: str
    description: str | None = None
    order: int
    estimated_days: int

    model_config = {"from_attributes": True}


class DomainDetail(DomainBrief):
    """Domain with nested topics."""
    topics: list[TopicBrief] = []


class DomainFull(DomainBrief):
    """Domain with fully nested topics and objectives."""
    topics: list[TopicDetail] = []


# ── Skill Layer ──────────────────────────────────────────────────

class SkillLayerBrief(BaseModel):
    """Skill layer without nested domains."""
    id: int
    name: str
    description: str | None = None
    order: int
    estimated_days: int

    model_config = {"from_attributes": True}


class SkillLayerDetail(SkillLayerBrief):
    """Skill layer with nested domains."""
    domains: list[DomainBrief] = []


# ── Phase ────────────────────────────────────────────────────────

class PhaseBrief(BaseModel):
    """Phase without nested skill layers."""
    id: int
    name: str
    description: str | None = None
    order: int

    model_config = {"from_attributes": True}


class PhaseDetail(PhaseBrief):
    """Phase with nested skill layers."""
    skill_layers: list[SkillLayerBrief] = []


class PhaseFull(PhaseBrief):
    """Phase with fully nested skill layers and domains."""
    skill_layers: list[SkillLayerDetail] = []


# ── Curriculum Overview ──────────────────────────────────────────

class CurriculumStats(BaseModel):
    """High-level curriculum statistics."""
    total_phases: int
    total_skill_layers: int
    total_domains: int
    total_topics: int
    total_objectives: int
    total_days: int


# ── Roadmap & Navigation Schemas ─────────────────────────────────

class TopicRoadmapItem(BaseModel):
    """Individual topic in the roadmap with user task status."""
    id: int
    name: str
    description: str | None = None
    order: int
    day_number: int | None = None
    estimated_hours: float
    difficulty: str
    objectives_count: int = 0
    objectives: list[LearningObjectiveResponse] = []
    task_id: int | None = None
    status: str | None = None  # 'todo', 'in_progress', 'completed', 'blocked', or None if unstarted

    model_config = {"from_attributes": True}


class DomainRoadmapItem(BaseModel):
    """Domain within the roadmap including day range and progress."""
    id: int
    name: str
    description: str | None = None
    order: int
    estimated_days: int
    topic_count: int = 0
    day_start: int | None = None
    day_end: int | None = None
    total_hours: float = 0.0
    completed_topics: int = 0
    progress_percent: float = 0.0

    model_config = {"from_attributes": True}


class SkillLayerRoadmapItem(BaseModel):
    """Skill layer containing its constituent domains and aggregate progress."""
    id: int
    name: str
    description: str | None = None
    order: int
    estimated_days: int
    domain_count: int = 0
    total_topics: int = 0
    completed_topics: int = 0
    progress_percent: float = 0.0
    domains: list[DomainRoadmapItem] = []

    model_config = {"from_attributes": True}


class PhaseRoadmapItem(BaseModel):
    """Phase containing skill layers and progress."""
    id: int
    name: str
    description: str | None = None
    order: int
    estimated_weeks: int | None = None
    total_topics: int = 0
    completed_topics: int = 0
    progress_percent: float = 0.0
    skill_layers: list[SkillLayerRoadmapItem] = []

    model_config = {"from_attributes": True}


class RoadmapResponse(BaseModel):
    """Full curriculum roadmap structure with user progress."""
    total_phases: int
    total_skill_layers: int
    total_domains: int
    total_topics: int
    total_days: int
    completed_topics: int = 0
    progress_percent: float = 0.0
    phases: list[PhaseRoadmapItem] = []


class DomainTopicsResponse(BaseModel):
    """List of topics with objectives and status for a single domain."""
    domain_id: int
    domain_name: str
    domain_description: str | None = None
    day_start: int | None = None
    day_end: int | None = None
    total_topics: int = 0
    completed_topics: int = 0
    progress_percent: float = 0.0
    topics: list[TopicRoadmapItem] = []
