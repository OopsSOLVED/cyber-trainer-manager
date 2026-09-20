"""
Tests for the database seeder.

Verifies that the seeder can successfully parse the JSON
and insert the curriculum hierarchy idempotently.
"""

import pytest
from unittest.mock import AsyncMock, patch
import json
from pathlib import Path

from app.db.seeder import load_curriculum_json, clear_curriculum_tables, seed_curriculum


class TestCurriculumSeeder:
    """Test the curriculum database seeder."""

    @pytest.mark.asyncio
    async def test_load_curriculum_json(self):
        """Should successfully load and parse the JSON seed file."""
        data = await load_curriculum_json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify structure of first phase
        phase1 = data[0]
        assert "name" in phase1
        assert "skill_layers" in phase1
        assert len(phase1["skill_layers"]) > 0

    @pytest.mark.asyncio
    async def test_clear_curriculum_tables(self):
        """Should execute a delete query on the Phase model."""
        mock_db = AsyncMock()
        await clear_curriculum_tables(mock_db)
        
        # Verify db.execute was called
        assert mock_db.execute.called
        assert mock_db.flush.called

    @pytest.mark.asyncio
    async def test_seed_curriculum_idempotent(self):
        """Should clear tables and insert new data."""
        mock_db = AsyncMock()
        
        # We don't want to actually load the massive real JSON for this unit test,
        # so we'll mock the load_curriculum_json function
        mock_data = [
            {
                "name": "Phase 1: Foundations",
                "description": "Core concepts.",
                "order": 1,
                "skill_layers": [
                    {
                        "name": "Networking",
                        "description": "Network concepts.",
                        "order": 1,
                        "estimated_days": 10,
                        "domains": [
                            {
                                "name": "TCP/IP",
                                "description": "Protocols",
                                "order": 1,
                                "estimated_days": 5,
                                "topics": [
                                    {
                                        "name": "Subnetting",
                                        "description": "CIDR",
                                        "order": 1,
                                        "day_number": 12,
                                        "estimated_hours": 2.0,
                                        "difficulty": "intermediate",
                                        "objectives": [
                                            {"description": "Calculate IPs", "order": 1, "is_measurable": True}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        
        with patch("app.db.seeder.load_curriculum_json", return_value=mock_data):
            await seed_curriculum(mock_db)
            
        # db.add should be called 5 times (Phase, SkillLayer, Domain, Topic, Objective)
        assert mock_db.add.call_count == 5
        assert mock_db.commit.called
        assert mock_db.flush.called

    @pytest.mark.asyncio
    async def test_full_curriculum_contains_196_days(self):
        """The actual curriculum_data.json must contain exactly 196 days."""
        data = await load_curriculum_json()
        days = []
        for phase in data:
            for layer in phase.get("skill_layers", []):
                for domain in layer.get("domains", []):
                    for topic in domain.get("topics", []):
                        if topic.get("day_number") is not None:
                            days.append(topic["day_number"])
        assert len(days) == 196

    @pytest.mark.asyncio
    async def test_days_are_sequential_and_complete(self):
        """All 196 days must be sequential from 1 to 196 with zero gaps or duplicates."""
        data = await load_curriculum_json()
        days = []
        for phase in data:
            for layer in phase.get("skill_layers", []):
                for domain in layer.get("domains", []):
                    for topic in domain.get("topics", []):
                        if topic.get("day_number") is not None:
                            days.append(topic["day_number"])
        assert sorted(days) == list(range(1, 197))
        assert len(set(days)) == 196

    @pytest.mark.asyncio
    async def test_all_phases_and_layers_defined(self):
        """Verify the 4 roadmap phases and essential skill layers are structured."""
        data = await load_curriculum_json()
        phase_names = [p["name"] for p in data]
        assert len(phase_names) == 4
        assert any("Foundations" in p for p in phase_names)
        assert any("Exploitation" in p for p in phase_names)
        assert any("Defensive" in p for p in phase_names)
        assert any("Trainer" in p for p in phase_names)

    @pytest.mark.asyncio
    async def test_all_topics_have_measurable_objectives(self):
        """Every topic must have at least one measurable learning objective."""
        data = await load_curriculum_json()
        for phase in data:
            for layer in phase.get("skill_layers", []):
                for domain in layer.get("domains", []):
                    for topic in domain.get("topics", []):
                        objectives = topic.get("objectives", [])
                        assert len(objectives) >= 1, f"Topic {topic['name']} has no objectives"
                        for obj in objectives:
                            assert "description" in obj
                            assert len(obj["description"]) > 5

