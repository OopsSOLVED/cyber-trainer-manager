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


# ── Full Roadmap & Progress ──────────────────────────────────────

async def get_roadmap_with_progress(
    db: AsyncSession,
    user_id: int | None = None,
) -> dict:
    """
    Get the entire curriculum roadmap hierarchy with live progress metrics.
    Calculates completed topic counts and completion percentages from actual
    database tasks for the specified user.
    """
    from app.models.task import Task, TaskStatus

    # Fetch phases with nested skill layers, domains, and topics
    result = await db.execute(
        select(Phase)
        .where(Phase.is_active.is_(True))
        .options(
            selectinload(Phase.skill_layers)
            .selectinload(SkillLayer.domains)
            .selectinload(Domain.topics)
        )
        .order_by(Phase.order)
    )
    phases = list(result.scalars().all())

    # Get completed topic IDs for the user
    completed_topic_ids: set[int] = set()
    if user_id:
        tasks_res = await db.execute(
            select(Task.topic_id).where(
                Task.user_id == user_id,
                Task.status == TaskStatus.COMPLETED,
            )
        )
        completed_topic_ids = set(tasks_res.scalars().all())

    phases_data = []
    global_total_topics = 0
    global_completed_topics = 0
    max_day = 0

    for phase in phases:
        layers_data = []
        phase_total_topics = 0
        phase_completed_topics = 0

        for layer in sorted(phase.skill_layers, key=lambda l: l.order):
            domains_data = []
            layer_total_topics = 0
            layer_completed_topics = 0

            for domain in sorted(layer.domains, key=lambda d: d.order):
                topics = domain.topics or []
                topic_count = len(topics)
                domain_completed = sum(1 for t in topics if t.id in completed_topic_ids)
                total_hours = sum(t.estimated_hours for t in topics)
                
                day_nums = [t.day_number for t in topics if t.day_number is not None]
                day_start = min(day_nums) if day_nums else None
                day_end = max(day_nums) if day_nums else None
                if day_end and day_end > max_day:
                    max_day = day_end

                progress_percent = (
                    round((domain_completed / topic_count * 100.0), 1)
                    if topic_count > 0
                    else 0.0
                )

                domains_data.append({
                    "id": domain.id,
                    "name": domain.name,
                    "description": domain.description,
                    "order": domain.order,
                    "estimated_days": domain.estimated_days,
                    "topic_count": topic_count,
                    "day_start": day_start,
                    "day_end": day_end,
                    "total_hours": round(total_hours, 1),
                    "completed_topics": domain_completed,
                    "progress_percent": progress_percent,
                })

                layer_total_topics += topic_count
                layer_completed_topics += domain_completed

            layer_progress = (
                round((layer_completed_topics / layer_total_topics * 100.0), 1)
                if layer_total_topics > 0
                else 0.0
            )

            layers_data.append({
                "id": layer.id,
                "name": layer.name,
                "description": layer.description,
                "order": layer.order,
                "estimated_days": layer.estimated_days,
                "domain_count": len(domains_data),
                "total_topics": layer_total_topics,
                "completed_topics": layer_completed_topics,
                "progress_percent": layer_progress,
                "domains": domains_data,
            })

            phase_total_topics += layer_total_topics
            phase_completed_topics += layer_completed_topics

        phase_progress = (
            round((phase_completed_topics / phase_total_topics * 100.0), 1)
            if phase_total_topics > 0
            else 0.0
        )

        estimated_weeks = max(1, round(phase_total_topics / 7)) if phase_total_topics > 0 else 0

        phases_data.append({
            "id": phase.id,
            "name": phase.name,
            "description": phase.description,
            "order": phase.order,
            "estimated_weeks": estimated_weeks,
            "total_topics": phase_total_topics,
            "completed_topics": phase_completed_topics,
            "progress_percent": phase_progress,
            "skill_layers": layers_data,
        })

        global_total_topics += phase_total_topics
        global_completed_topics += phase_completed_topics

    total_layers = sum(len(p["skill_layers"]) for p in phases_data)
    total_domains = sum(len(l["domains"]) for p in phases_data for l in p["skill_layers"])
    global_progress = (
        round((global_completed_topics / global_total_topics * 100.0), 1)
        if global_total_topics > 0
        else 0.0
    )

    return {
        "total_phases": len(phases_data),
        "total_skill_layers": total_layers,
        "total_domains": total_domains,
        "total_topics": global_total_topics,
        "total_days": max_day or 196,
        "completed_topics": global_completed_topics,
        "progress_percent": global_progress,
        "phases": phases_data,
    }


async def get_domain_topics_with_status(
    db: AsyncSession,
    domain_id: int,
    user_id: int | None = None,
) -> dict | None:
    """
    Get all topics for a domain including objectives and the user's task status.
    """
    from app.models.task import Task

    domain_res = await db.execute(
        select(Domain)
        .where(Domain.id == domain_id)
        .options(
            selectinload(Domain.topics).selectinload(Topic.objectives)
        )
    )
    domain = domain_res.scalar_one_or_none()
    if not domain:
        return None

    user_tasks_map: dict[int, Task] = {}
    if user_id and domain.topics:
        topic_ids = [t.id for t in domain.topics]
        tasks_res = await db.execute(
            select(Task).where(
                Task.user_id == user_id,
                Task.topic_id.in_(topic_ids),
            )
        )
        for task in tasks_res.scalars().all():
            user_tasks_map[task.topic_id] = task

    topics_data = []
    completed_count = 0
    sorted_topics = sorted(
        domain.topics,
        key=lambda t: (t.day_number if t.day_number is not None else 9999, t.order),
    )

    for topic in sorted_topics:
        task = user_tasks_map.get(topic.id)
        task_status = task.status.value if task else None
        if task_status == "completed":
            completed_count += 1

        topics_data.append({
            "id": topic.id,
            "name": topic.name,
            "description": topic.description,
            "order": topic.order,
            "day_number": topic.day_number,
            "estimated_hours": topic.estimated_hours,
            "difficulty": topic.difficulty,
            "objectives_count": len(topic.objectives),
            "objectives": topic.objectives,
            "task_id": task.id if task else None,
            "status": task_status,
        })

    day_nums = [t.day_number for t in domain.topics if t.day_number is not None]
    day_start = min(day_nums) if day_nums else None
    day_end = max(day_nums) if day_nums else None
    total_topics = len(topics_data)
    progress_percent = (
        round((completed_count / total_topics * 100.0), 1)
        if total_topics > 0
        else 0.0
    )

    return {
        "domain_id": domain.id,
        "domain_name": domain.name,
        "domain_description": domain.description,
        "day_start": day_start,
        "day_end": day_end,
        "total_topics": total_topics,
        "completed_topics": completed_count,
        "progress_percent": progress_percent,
        "topics": topics_data,
    }
