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
