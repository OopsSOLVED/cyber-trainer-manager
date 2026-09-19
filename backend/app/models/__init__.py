"""
Database models package.

All ORM models are imported here so Alembic can discover them
for auto-generating migrations.
"""

from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.curriculum import (  # noqa: F401
    Phase,
    SkillLayer,
    Domain,
    Topic,
    LearningObjective,
)

from app.models.task import Task, Subtask  # noqa: F401
