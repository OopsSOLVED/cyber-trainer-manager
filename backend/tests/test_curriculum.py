"""
Curriculum model and endpoint tests.

Tests for curriculum ORM models, schemas, and API endpoints.
Uses mocked database fixtures — no live PostgreSQL required.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone


# ═══════════════════════════════════════════════════════════════
# Model Tests
# ═══════════════════════════════════════════════════════════════

class TestCurriculumModels:
    """Test curriculum ORM model definitions."""

    def test_phase_model_exists(self):
        """Phase model should be importable."""
        from app.models.curriculum import Phase
        assert Phase.__tablename__ == "phases"

    def test_skill_layer_model_exists(self):
        """SkillLayer model should be importable."""
        from app.models.curriculum import SkillLayer
        assert SkillLayer.__tablename__ == "skill_layers"

    def test_domain_model_exists(self):
        """Domain model should be importable."""
        from app.models.curriculum import Domain
        assert Domain.__tablename__ == "domains"

    def test_topic_model_exists(self):
        """Topic model should be importable."""
        from app.models.curriculum import Topic
        assert Topic.__tablename__ == "topics"

    def test_learning_objective_model_exists(self):
        """LearningObjective model should be importable."""
        from app.models.curriculum import LearningObjective
        assert LearningObjective.__tablename__ == "learning_objectives"

    def test_all_models_registered(self):
        """All curriculum models should be in the models package."""
        from app.models import Phase, SkillLayer, Domain, Topic, LearningObjective
        assert Phase is not None
        assert SkillLayer is not None
        assert Domain is not None
        assert Topic is not None
        assert LearningObjective is not None


# ═══════════════════════════════════════════════════════════════
# Schema Tests
# ═══════════════════════════════════════════════════════════════

class TestCurriculumSchemas:
    """Test Pydantic schema validation."""

    def test_phase_brief_schema(self):
        """PhaseBrief should accept valid phase data."""
        from app.schemas.curriculum import PhaseBrief
        data = PhaseBrief(id=1, name="Foundation", description="Basics", order=1)
        assert data.name == "Foundation"

    def test_topic_brief_schema(self):
        """TopicBrief should accept valid topic data."""
        from app.schemas.curriculum import TopicBrief
        data = TopicBrief(
            id=1, name="Subnetting", order=1,
            day_number=5, estimated_hours=2.0, difficulty="intermediate",
        )
        assert data.day_number == 5
        assert data.difficulty == "intermediate"

    def test_curriculum_stats_schema(self):
        """CurriculumStats should accept aggregate data."""
        from app.schemas.curriculum import CurriculumStats
        stats = CurriculumStats(
            total_phases=4, total_skill_layers=13,
            total_domains=50, total_topics=200,
            total_objectives=600, total_days=196,
        )
        assert stats.total_days == 196

    def test_topic_detail_with_objectives(self):
        """TopicDetail should accept nested objectives."""
        from app.schemas.curriculum import TopicDetail, LearningObjectiveResponse
        obj = LearningObjectiveResponse(id=1, description="Calculate CIDR", order=1, is_measurable=True)
        topic = TopicDetail(
            id=1, name="Subnetting", order=1,
            estimated_hours=2.0, difficulty="intermediate",
            objectives=[obj],
        )
        assert len(topic.objectives) == 1


# ═══════════════════════════════════════════════════════════════
# Endpoint Tests
# ═══════════════════════════════════════════════════════════════

def _mock_phase(id=1, name="Foundation", order=1, description="Basics", skill_layers=None):
    """Create a mock Phase object."""
    phase = MagicMock()
    phase.id = id
    phase.name = name
    phase.order = order
    phase.description = description
    phase.is_active = True
    phase.created_at = datetime.now(timezone.utc)
    phase.updated_at = datetime.now(timezone.utc)
    phase.skill_layers = skill_layers or []
    return phase


def _mock_skill_layer(id=1, name="Networking", order=1, estimated_days=20, domains=None):
    """Create a mock SkillLayer object."""
    layer = MagicMock()
    layer.id = id
    layer.name = name
    layer.order = order
    layer.estimated_days = estimated_days
    layer.description = None
    layer.is_active = True
    layer.domains = domains or []
    return layer


def _mock_domain(id=1, name="TCP/IP", order=1, estimated_days=5, topics=None):
    """Create a mock Domain object."""
    domain = MagicMock()
    domain.id = id
    domain.name = name
    domain.order = order
    domain.estimated_days = estimated_days
    domain.description = None
    domain.is_active = True
    domain.topics = topics or []
    return domain


def _mock_topic(id=1, name="Subnetting", order=1, day_number=5, objectives=None):
    """Create a mock Topic object."""
    topic = MagicMock()
    topic.id = id
    topic.name = name
    topic.order = order
    topic.day_number = day_number
    topic.estimated_hours = 2.0
    topic.difficulty = "intermediate"
    topic.description = None
    topic.is_active = True
    topic.objectives = objectives or []
    return topic


class TestCurriculumEndpoints:
    """Test curriculum API endpoints."""

    @pytest.mark.asyncio
    async def test_list_phases_empty(self, client):
        """GET /curriculum/phases should return empty list when no data."""
        with patch("app.api.v1.curriculum.get_all_phases", new_callable=AsyncMock, return_value=[]):
            response = await client.get("/api/v1/curriculum/phases")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_phases_with_data(self, client):
        """GET /curriculum/phases should return phases."""
        phases = [_mock_phase(1, "Foundation", 1), _mock_phase(2, "Offensive", 2)]
        with patch("app.api.v1.curriculum.get_all_phases", new_callable=AsyncMock, return_value=phases):
            response = await client.get("/api/v1/curriculum/phases")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Foundation"
        assert data[1]["name"] == "Offensive"

    @pytest.mark.asyncio
    async def test_get_phase_success(self, client):
        """GET /curriculum/phases/1 should return phase with skill layers."""
        layer = _mock_skill_layer()
        phase = _mock_phase(skill_layers=[layer])
        with patch("app.api.v1.curriculum.get_phase_by_id", new_callable=AsyncMock, return_value=phase):
            response = await client.get("/api/v1/curriculum/phases/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Foundation"
        assert len(data["skill_layers"]) == 1

    @pytest.mark.asyncio
    async def test_get_phase_not_found(self, client):
        """GET /curriculum/phases/999 should return 404."""
        with patch("app.api.v1.curriculum.get_phase_by_id", new_callable=AsyncMock, return_value=None):
            response = await client.get("/api/v1/curriculum/phases/999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_skill_layer_success(self, client):
        """GET /curriculum/skill-layers/1 should return layer with domains."""
        domain = _mock_domain()
        layer = _mock_skill_layer(domains=[domain])
        with patch("app.api.v1.curriculum.get_skill_layer_by_id", new_callable=AsyncMock, return_value=layer):
            response = await client.get("/api/v1/curriculum/skill-layers/1")
        assert response.status_code == 200
        assert len(response.json()["domains"]) == 1

    @pytest.mark.asyncio
    async def test_get_skill_layer_not_found(self, client):
        """GET /curriculum/skill-layers/999 should return 404."""
        with patch("app.api.v1.curriculum.get_skill_layer_by_id", new_callable=AsyncMock, return_value=None):
            response = await client.get("/api/v1/curriculum/skill-layers/999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_domain_success(self, client):
        """GET /curriculum/domains/1 should return domain with topics."""
        topic = _mock_topic()
        domain = _mock_domain(topics=[topic])
        with patch("app.api.v1.curriculum.get_domain_by_id", new_callable=AsyncMock, return_value=domain):
            response = await client.get("/api/v1/curriculum/domains/1")
        assert response.status_code == 200
        assert len(response.json()["topics"]) == 1

    @pytest.mark.asyncio
    async def test_get_topic_success(self, client):
        """GET /curriculum/topics/1 should return topic with objectives."""
        obj = MagicMock()
        obj.id = 1
        obj.description = "Calculate CIDR"
        obj.order = 1
        obj.is_measurable = True
        topic = _mock_topic(objectives=[obj])
        with patch("app.api.v1.curriculum.get_topic_by_id", new_callable=AsyncMock, return_value=topic):
            response = await client.get("/api/v1/curriculum/topics/1")
        assert response.status_code == 200
        data = response.json()
        assert len(data["objectives"]) == 1
        assert data["objectives"][0]["description"] == "Calculate CIDR"

    @pytest.mark.asyncio
    async def test_get_day_topics(self, client):
        """GET /curriculum/day/5 should return topics for that day."""
        topics = [_mock_topic(day_number=5)]
        with patch("app.api.v1.curriculum.get_topics_by_day", new_callable=AsyncMock, return_value=topics):
            response = await client.get("/api/v1/curriculum/day/5")
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.asyncio
    async def test_get_day_invalid(self, client):
        """GET /curriculum/day/0 should return 400."""
        response = await client.get("/api/v1/curriculum/day/0")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_curriculum_stats(self, client):
        """GET /curriculum/stats should return aggregate counts."""
        stats = {
            "total_phases": 4, "total_skill_layers": 13,
            "total_domains": 50, "total_topics": 200,
            "total_objectives": 600, "total_days": 196,
        }
        with patch("app.api.v1.curriculum.get_curriculum_stats", new_callable=AsyncMock, return_value=stats):
            response = await client.get("/api/v1/curriculum/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_days"] == 196
        assert data["total_skill_layers"] == 13

    @pytest.mark.asyncio
    async def test_phase_full_hierarchy(self, client):
        """GET /curriculum/phases/1/full should return nested hierarchy."""
        domain = _mock_domain()
        layer = _mock_skill_layer(domains=[domain])
        phase = _mock_phase(skill_layers=[layer])
        with patch("app.api.v1.curriculum.get_phase_full", new_callable=AsyncMock, return_value=phase):
            response = await client.get("/api/v1/curriculum/phases/1/full")
        assert response.status_code == 200
        data = response.json()
        assert len(data["skill_layers"]) == 1
        assert len(data["skill_layers"][0]["domains"]) == 1

    @pytest.mark.asyncio
    async def test_get_roadmap_endpoint(self, client):
        """GET /curriculum/roadmap should return full hierarchy with progress."""
        roadmap_data = {
            "total_phases": 4,
            "total_skill_layers": 10,
            "total_domains": 28,
            "total_topics": 196,
            "total_days": 196,
            "completed_topics": 14,
            "progress_percent": 7.1,
            "phases": [
                {
                    "id": 1,
                    "name": "Foundations",
                    "description": "Core computer and network basics",
                    "order": 1,
                    "estimated_weeks": 7,
                    "total_topics": 49,
                    "completed_topics": 14,
                    "progress_percent": 28.6,
                    "skill_layers": [
                        {
                            "id": 1,
                            "name": "Computer Foundations",
                            "description": "Hardware and OS",
                            "order": 1,
                            "estimated_days": 14,
                            "domain_count": 2,
                            "total_topics": 14,
                            "completed_topics": 14,
                            "progress_percent": 100.0,
                            "domains": [
                                {
                                    "id": 1,
                                    "name": "Hardware Architecture",
                                    "description": "CPU, RAM, Storage",
                                    "order": 1,
                                    "estimated_days": 7,
                                    "topic_count": 7,
                                    "day_start": 1,
                                    "day_end": 7,
                                    "total_hours": 21.0,
                                    "completed_topics": 7,
                                    "progress_percent": 100.0,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        with patch("app.api.v1.curriculum.get_roadmap_with_progress", new_callable=AsyncMock, return_value=roadmap_data):
            response = await client.get("/api/v1/curriculum/roadmap")
        assert response.status_code == 200
        data = response.json()
        assert data["total_phases"] == 4
        assert data["total_domains"] == 28
        assert data["completed_topics"] == 14
        assert len(data["phases"]) == 1
        assert len(data["phases"][0]["skill_layers"]) == 1
        assert data["phases"][0]["skill_layers"][0]["domains"][0]["progress_percent"] == 100.0

    @pytest.mark.asyncio
    async def test_get_domain_topics_with_status_success(self, client):
        """GET /curriculum/domains/{id}/topics-with-status should return topics."""
        domain_topics_data = {
            "domain_id": 1,
            "domain_name": "Hardware Architecture",
            "domain_description": "CPU, RAM, Storage",
            "day_start": 1,
            "day_end": 7,
            "total_topics": 1,
            "completed_topics": 1,
            "progress_percent": 100.0,
            "topics": [
                {
                    "id": 1,
                    "name": "CPU Architecture & Registers",
                    "description": "x86/x64 registers and instruction cycles",
                    "order": 1,
                    "day_number": 1,
                    "estimated_hours": 3.0,
                    "difficulty": "beginner",
                    "objectives_count": 3,
                    "objectives": [],
                    "task_id": 101,
                    "status": "completed",
                }
            ],
        }
        with patch("app.api.v1.curriculum.get_domain_topics_with_status", new_callable=AsyncMock, return_value=domain_topics_data):
            response = await client.get("/api/v1/curriculum/domains/1/topics-with-status")
        assert response.status_code == 200
        data = response.json()
        assert data["domain_name"] == "Hardware Architecture"
        assert len(data["topics"]) == 1
        assert data["topics"][0]["status"] == "completed"

    @pytest.mark.asyncio
    async def test_get_domain_topics_with_status_not_found(self, client):
        """GET /curriculum/domains/999/topics-with-status should 404 if domain missing."""
        with patch("app.api.v1.curriculum.get_domain_topics_with_status", new_callable=AsyncMock, return_value=None):
            response = await client.get("/api/v1/curriculum/domains/999/topics-with-status")
        assert response.status_code == 404
