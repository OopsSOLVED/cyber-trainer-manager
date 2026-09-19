"""
Curriculum repository.

Data access layer for curriculum model operations.
All database queries for the curriculum hierarchy are centralized here.
"""

import logging

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.curriculum import (
    Phase,
    SkillLayer,
    Domain,
    Topic,
    LearningObjective,
)

logger = logging.getLogger(__name__)


# ── Phase Queries ────────────────────────────────────────────────

async def get_all_phases(db: AsyncSession) -> list[Phase]:
    """Get all phases ordered by position."""
    result = await db.execute(
        select(Phase)
        .where(Phase.is_active.is_(True))
        .order_by(Phase.order)
    )
    return list(result.scalars().all())


async def get_phase_by_id(db: AsyncSession, phase_id: int) -> Phase | None:
    """Get a phase with its skill layers loaded."""
    result = await db.execute(
        select(Phase)
        .where(Phase.id == phase_id)
        .options(selectinload(Phase.skill_layers))
    )
    return result.scalar_one_or_none()


async def get_phase_full(db: AsyncSession, phase_id: int) -> Phase | None:
    """Get a phase with skill layers and domains loaded."""
    result = await db.execute(
        select(Phase)
        .where(Phase.id == phase_id)
        .options(
            selectinload(Phase.skill_layers)
            .selectinload(SkillLayer.domains)
        )
    )
    return result.scalar_one_or_none()


# ── Skill Layer Queries ──────────────────────────────────────────

async def get_skill_layer_by_id(db: AsyncSession, layer_id: int) -> SkillLayer | None:
    """Get a skill layer with its domains loaded."""
    result = await db.execute(
        select(SkillLayer)
        .where(SkillLayer.id == layer_id)
        .options(selectinload(SkillLayer.domains))
    )
    return result.scalar_one_or_none()


# ── Domain Queries ───────────────────────────────────────────────

async def get_domain_by_id(db: AsyncSession, domain_id: int) -> Domain | None:
    """Get a domain with its topics loaded."""
    result = await db.execute(
        select(Domain)
        .where(Domain.id == domain_id)
        .options(selectinload(Domain.topics))
    )
    return result.scalar_one_or_none()


# ── Topic Queries ────────────────────────────────────────────────

async def get_topic_by_id(db: AsyncSession, topic_id: int) -> Topic | None:
    """Get a topic with its learning objectives loaded."""
    result = await db.execute(
        select(Topic)
        .where(Topic.id == topic_id)
        .options(selectinload(Topic.objectives))
    )
    return result.scalar_one_or_none()


async def get_topics_by_day(db: AsyncSession, day_number: int) -> list[Topic]:
    """Get all topics for a specific day in the 196-day plan."""
    result = await db.execute(
        select(Topic)
        .where(Topic.day_number == day_number, Topic.is_active.is_(True))
        .options(selectinload(Topic.objectives))
        .order_by(Topic.order)
    )
    return list(result.scalars().all())


# ── Statistics ───────────────────────────────────────────────────

async def get_curriculum_stats(db: AsyncSession) -> dict:
    """Get aggregate statistics for the entire curriculum."""
    phases = await db.execute(select(func.count(Phase.id)).where(Phase.is_active.is_(True)))
    layers = await db.execute(select(func.count(SkillLayer.id)).where(SkillLayer.is_active.is_(True)))
    domains = await db.execute(select(func.count(Domain.id)).where(Domain.is_active.is_(True)))
    topics = await db.execute(select(func.count(Topic.id)).where(Topic.is_active.is_(True)))
    objectives = await db.execute(select(func.count(LearningObjective.id)).where(LearningObjective.is_active.is_(True)))
    max_day = await db.execute(select(func.max(Topic.day_number)))

    return {
        "total_phases": phases.scalar_one() or 0,
        "total_skill_layers": layers.scalar_one() or 0,
        "total_domains": domains.scalar_one() or 0,
        "total_topics": topics.scalar_one() or 0,
        "total_objectives": objectives.scalar_one() or 0,
        "total_days": max_day.scalar_one() or 0,
    }
