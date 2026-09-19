"""
Curriculum endpoints.

Read-only endpoints for navigating the curriculum hierarchy.
Admin write endpoints will be added in a future session.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.curriculum import (
    get_all_phases,
    get_phase_by_id,
    get_phase_full,
    get_skill_layer_by_id,
    get_domain_by_id,
    get_topic_by_id,
    get_topics_by_day,
    get_curriculum_stats,
)
from app.schemas.curriculum import (
    PhaseBrief,
    PhaseDetail,
    PhaseFull,
    SkillLayerDetail,
    DomainDetail,
    TopicDetail,
    CurriculumStats,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.get(
    "/stats",
    response_model=CurriculumStats,
    summary="Curriculum statistics",
    description="Returns aggregate counts for all curriculum elements.",
)
async def curriculum_stats(db: AsyncSession = Depends(get_db)):
    """Get high-level curriculum statistics."""
    stats = await get_curriculum_stats(db)
    return stats


@router.get(
    "/phases",
    response_model=list[PhaseBrief],
    summary="List all phases",
    description="Returns all curriculum phases in order.",
)
async def list_phases(db: AsyncSession = Depends(get_db)):
    """List all curriculum phases."""
    phases = await get_all_phases(db)
    return phases


@router.get(
    "/phases/{phase_id}",
    response_model=PhaseDetail,
    summary="Get phase with skill layers",
    description="Returns a phase with its child skill layers.",
)
async def get_phase(phase_id: int, db: AsyncSession = Depends(get_db)):
    """Get a phase with its skill layers."""
    phase = await get_phase_by_id(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phase not found")
    return phase


@router.get(
    "/phases/{phase_id}/full",
    response_model=PhaseFull,
    summary="Get phase with full hierarchy",
    description="Returns a phase with skill layers and domains nested.",
)
async def get_phase_hierarchy(phase_id: int, db: AsyncSession = Depends(get_db)):
    """Get a phase with full hierarchy (skill layers + domains)."""
    phase = await get_phase_full(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phase not found")
    return phase


@router.get(
    "/skill-layers/{layer_id}",
    response_model=SkillLayerDetail,
    summary="Get skill layer with domains",
    description="Returns a skill layer with its child domains.",
)
async def get_skill_layer(layer_id: int, db: AsyncSession = Depends(get_db)):
    """Get a skill layer with its domains."""
    layer = await get_skill_layer_by_id(db, layer_id)
    if not layer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill layer not found")
    return layer


@router.get(
    "/domains/{domain_id}",
    response_model=DomainDetail,
    summary="Get domain with topics",
    description="Returns a domain with its child topics.",
)
async def get_domain(domain_id: int, db: AsyncSession = Depends(get_db)):
    """Get a domain with its topics."""
    domain = await get_domain_by_id(db, domain_id)
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    return domain


@router.get(
    "/topics/{topic_id}",
    response_model=TopicDetail,
    summary="Get topic with objectives",
    description="Returns a topic with its learning objectives.",
)
async def get_topic(topic_id: int, db: AsyncSession = Depends(get_db)):
    """Get a topic with its learning objectives."""
    topic = await get_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


@router.get(
    "/day/{day_number}",
    response_model=list[TopicDetail],
    summary="Get topics for a specific day",
    description="Returns all topics scheduled for a day in the 196-day plan.",
)
async def get_day_topics(day_number: int, db: AsyncSession = Depends(get_db)):
    """Get all topics for a specific day number."""
    if day_number < 1 or day_number > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day number must be between 1 and 365",
        )
    topics = await get_topics_by_day(db, day_number)
    return topics
