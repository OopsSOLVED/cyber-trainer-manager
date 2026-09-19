"""
Curriculum Database Seeder.

Parses curriculum_data.json and populates the database with
the 196-day cybersecurity roadmap hierarchy.
"""

import json
import logging
from pathlib import Path

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import Phase, SkillLayer, Domain, Topic, LearningObjective

logger = logging.getLogger(__name__)


async def load_curriculum_json() -> list[dict]:
    """Load the curriculum JSON file."""
    seed_file = Path(__file__).parent / "seeds" / "curriculum_data.json"
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_file}")
        
    with open(seed_file, "r", encoding="utf-8") as f:
        return json.load(f)


async def clear_curriculum_tables(db: AsyncSession):
    """Clear existing curriculum data (idempotency)."""
    logger.info("Clearing existing curriculum data...")
    # Because of CASCADE deletes, deleting Phases will delete everything below it.
    await db.execute(delete(Phase))
    await db.flush()


async def seed_curriculum(db: AsyncSession):
    """
    Seed the database with the curriculum hierarchy.
    Idempotent operation: clears existing data first.
    """
    data = await load_curriculum_json()
    await clear_curriculum_tables(db)
    
    logger.info("Seeding curriculum data...")
    
    for phase_data in data:
        # Create Phase
        phase = Phase(
            name=phase_data["name"],
            description=phase_data.get("description"),
            order=phase_data["order"],
        )
        db.add(phase)
        await db.flush()  # to get phase.id
        
        for layer_data in phase_data.get("skill_layers", []):
            # Create SkillLayer
            layer = SkillLayer(
                phase_id=phase.id,
                name=layer_data["name"],
                description=layer_data.get("description"),
                order=layer_data["order"],
                estimated_days=layer_data.get("estimated_days", 0),
            )
            db.add(layer)
            await db.flush()
            
            for domain_data in layer_data.get("domains", []):
                # Create Domain
                domain = Domain(
                    skill_layer_id=layer.id,
                    name=domain_data["name"],
                    description=domain_data.get("description"),
                    order=domain_data["order"],
                    estimated_days=domain_data.get("estimated_days", 0),
                )
                db.add(domain)
                await db.flush()
                
                for topic_data in domain_data.get("topics", []):
                    # Create Topic
                    topic = Topic(
                        domain_id=domain.id,
                        name=topic_data["name"],
                        description=topic_data.get("description"),
                        order=topic_data["order"],
                        day_number=topic_data.get("day_number"),
                        estimated_hours=topic_data.get("estimated_hours", 1.0),
                        difficulty=topic_data.get("difficulty", "intermediate"),
                    )
                    db.add(topic)
                    await db.flush()
                    
                    for obj_data in topic_data.get("objectives", []):
                        # Create LearningObjective
                        objective = LearningObjective(
                            topic_id=topic.id,
                            description=obj_data["description"],
                            order=obj_data["order"],
                            is_measurable=obj_data.get("is_measurable", True),
                        )
                        db.add(objective)
    
    await db.commit()
    logger.info("Curriculum seeding completed successfully!")
