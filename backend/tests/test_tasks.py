"""
Task and Subtask tests.

Tests for task ORM models, schemas, and API endpoints.
Uses mocked database fixtures — no live PostgreSQL required.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from app.models.task import TaskStatus


# ═══════════════════════════════════════════════════════════════
# Model Tests
# ═══════════════════════════════════════════════════════════════

class TestTaskModels:
    """Test task ORM model definitions."""

    def test_task_model_exists(self):
        """Task model should be importable."""
        from app.models.task import Task
        assert Task.__tablename__ == "tasks"

    def test_subtask_model_exists(self):
        """Subtask model should be importable."""
        from app.models.task import Subtask
        assert Subtask.__tablename__ == "subtasks"

    def test_task_status_enum(self):
        """TaskStatus enum should have expected values."""
        assert TaskStatus.TODO == "todo"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.BLOCKED == "blocked"
        assert TaskStatus.SKIPPED == "skipped"


# ═══════════════════════════════════════════════════════════════
# Schema Tests
# ═══════════════════════════════════════════════════════════════

class TestTaskSchemas:
    """Test Pydantic schema validation."""

    def test_task_generation_request(self):
        """TaskGenerationRequest should require valid day_number."""
        from app.schemas.task import TaskGenerationRequest
        from pydantic import ValidationError
        
        req = TaskGenerationRequest(day_number=1)
        assert req.day_number == 1
        
        with pytest.raises(ValidationError):
            TaskGenerationRequest(day_number=400)  # > 365
            
        with pytest.raises(ValidationError):
            TaskGenerationRequest(day_number=0)   # < 1

    def test_task_update_schema(self):
        """TaskUpdate should accept status and notes."""
        from app.schemas.task import TaskUpdate
        update = TaskUpdate(status=TaskStatus.IN_PROGRESS, notes="Started", actual_hours=1.5)
        assert update.status == TaskStatus.IN_PROGRESS
        assert update.notes == "Started"
        assert update.actual_hours == 1.5


# ═══════════════════════════════════════════════════════════════
# Endpoint Tests
# ═══════════════════════════════════════════════════════════════

def _mock_user(id=1, email="test@example.com"):
    user = MagicMock()
    user.id = id
    user.email = email
    user.is_active = True
    return user

def _mock_topic(id=1, name="Subnetting"):
    topic = MagicMock()
    topic.id = id
    topic.name = name
    topic.description = "Test topic"
    topic.order = 1
    topic.day_number = 1
    topic.estimated_hours = 2.0
    topic.difficulty = "intermediate"
    return topic

def _mock_learning_objective(id=1):
    lo = MagicMock()
    lo.id = id
    lo.description = "Learn something"
    lo.order = 1
    lo.is_measurable = True
    return lo

def _mock_subtask(id=1, task_id=1, lo_id=1):
    subtask = MagicMock()
    subtask.id = id
    subtask.task_id = task_id
    subtask.learning_objective_id = lo_id
    subtask.status = TaskStatus.TODO
    subtask.order = 1
    subtask.notes = None
    subtask.learning_objective = _mock_learning_objective(id=lo_id)
    return subtask

def _mock_task(id=1, user_id=1, topic_id=1, status=TaskStatus.TODO):
    task = MagicMock()
    task.id = id
    task.user_id = user_id
    task.topic_id = topic_id
    task.status = status
    task.notes = None
    task.estimated_hours = 2.0
    task.actual_hours = 0.0
    task.assigned_date = datetime.now(timezone.utc)
    task.completed_at = None
    task.topic = _mock_topic(id=topic_id)
    task.subtasks = [_mock_subtask(id=1, task_id=id, lo_id=1)]
    return task


class TestTaskEndpoints:
    """Test tasks API endpoints."""

    @pytest.fixture
    def authenticated_client(self, app, client):
        """Mock get_current_user dependency."""
        from app.api.deps import get_current_user
        app.dependency_overrides[get_current_user] = lambda: _mock_user(id=1)
        yield client
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_generate_tasks(self, authenticated_client):
        """POST /tasks/generate should return generated tasks."""
        tasks = [_mock_task(id=1)]
        with patch("app.api.v1.tasks.generate_tasks_for_day", new_callable=AsyncMock, return_value=tasks):
            response = await authenticated_client.post("/api/v1/tasks/generate", json={"day_number": 1})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["topic"]["name"] == "Subnetting"
        assert len(data[0]["subtasks"]) == 1

    @pytest.mark.asyncio
    async def test_get_today_tasks(self, authenticated_client):
        """GET /tasks/today should return today's tasks."""
        tasks = [_mock_task(id=1), _mock_task(id=2)]
        with patch("app.api.v1.tasks.get_user_tasks_for_day", new_callable=AsyncMock, return_value=tasks):
            response = await authenticated_client.get("/api/v1/tasks/today")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_update_task_success(self, authenticated_client):
        """PATCH /tasks/{id} should update task."""
        task = _mock_task(id=1, user_id=1)
        updated_task = _mock_task(id=1, user_id=1, status=TaskStatus.IN_PROGRESS)
        updated_task.notes = "Working on it"
        
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            with patch("app.api.v1.tasks.update_task", new_callable=AsyncMock, return_value=updated_task):
                response = await authenticated_client.patch(
                    "/api/v1/tasks/1",
                    json={"status": "in_progress", "notes": "Working on it"}
                )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
        assert response.json()["notes"] == "Working on it"

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, authenticated_client):
        """PATCH /tasks/{id} returns 404 if not found."""
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=None):
            response = await authenticated_client.patch(
                "/api/v1/tasks/999",
                json={"status": "in_progress"}
            )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_forbidden(self, authenticated_client):
        """PATCH /tasks/{id} returns 403 if task belongs to another user."""
        task = _mock_task(id=1, user_id=2)  # Different user
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            response = await authenticated_client.patch(
                "/api/v1/tasks/1",
                json={"status": "in_progress"}
            )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_subtask_success(self, authenticated_client):
        """PATCH /tasks/subtasks/{id} should update subtask."""
        subtask = _mock_subtask(id=1, task_id=1)
        task = _mock_task(id=1, user_id=1)
        
        updated_subtask = _mock_subtask(id=1, task_id=1)
        updated_subtask.status = TaskStatus.COMPLETED
        
        with patch("app.api.v1.tasks.get_subtask_by_id", new_callable=AsyncMock, return_value=subtask):
            with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
                with patch("app.api.v1.tasks.update_subtask", new_callable=AsyncMock, return_value=updated_subtask):
                    response = await authenticated_client.patch(
                        "/api/v1/tasks/subtasks/1",
                        json={"status": "completed"}
                    )
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    @pytest.mark.asyncio
    async def test_update_subtask_not_found(self, authenticated_client):
        """PATCH /tasks/subtasks/{id} returns 404 if not found."""
        with patch("app.api.v1.tasks.get_subtask_by_id", new_callable=AsyncMock, return_value=None):
            response = await authenticated_client.patch(
                "/api/v1/tasks/subtasks/999",
                json={"status": "completed"}
            )
        assert response.status_code == 404
