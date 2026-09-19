"""
Database models package.

All ORM models are imported here so Alembic can discover them
for auto-generating migrations.
"""

from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401

# Import all models here as they are created in future sessions:
# from app.models.curriculum import Phase, SkillLayer, Domain, ...  # Session 4
# from app.models.task import Task, Subtask, TaskDependency, ...  # Session 5
