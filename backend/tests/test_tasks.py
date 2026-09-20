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
        assert TaskStatus.NEEDS_REVIEW == "needs_review"

    def test_task_priority_enum(self):
        """TaskPriority enum should have expected values."""
        from app.models.task import TaskPriority
        assert TaskPriority.LOW == "low"
        assert TaskPriority.MEDIUM == "medium"
        assert TaskPriority.HIGH == "high"
        assert TaskPriority.CRITICAL == "critical"

    def test_task_type_enum(self):
        """TaskType enum should have expected values."""
        from app.models.task import TaskType
        assert TaskType.STUDY == "study"
        assert TaskType.PRACTICE == "practice"
        assert TaskType.LAB == "lab"
        assert TaskType.CTF == "ctf"
        assert TaskType.ASSESSMENT == "assessment"

    def test_task_dependency_model_exists(self):
        """TaskDependency model should be importable."""
        from app.models.task import TaskDependency
        assert TaskDependency.__tablename__ == "task_dependencies"


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

from app.models.task import TaskPriority, TaskType


def _mock_task(id=1, user_id=1, topic_id=1, status=TaskStatus.TODO):
    task = MagicMock()
    task.id = id
    task.user_id = user_id
    task.topic_id = topic_id
    task.status = status
    task.priority = TaskPriority.MEDIUM
    task.task_type = TaskType.STUDY
    task.notes = None
    task.estimated_hours = 2.0
    task.actual_hours = 0.0
    task.assigned_date = datetime.now(timezone.utc)
    task.due_date = None
    task.completed_at = None
    task.confidence_score = None
    task.review_date = None
    task.topic = _mock_topic(id=topic_id)
    task.subtasks = [_mock_subtask(id=1, task_id=id, lo_id=1)]
    task.dependencies = []
    task.prerequisite_task_ids = []
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

    @pytest.mark.asyncio
    async def test_update_task_dependency_blocked(self, authenticated_client):
        """PATCH /tasks/{id} returns 400 when completing a task with unmet dependencies."""
        task = _mock_task(id=1, user_id=1)
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            with patch(
                "app.api.v1.tasks.update_task",
                new_callable=AsyncMock,
                side_effect=ValueError("Cannot complete task 1: prerequisite task(s) [2] are not completed.")
            ):
                response = await authenticated_client.patch(
                    "/api/v1/tasks/1",
                    json={"status": "completed"}
                )
        assert response.status_code == 400
        assert "prerequisite" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_add_dependency_endpoint_success(self, authenticated_client):
        """POST /tasks/{id}/dependencies successfully adds a prerequisite dependency."""
        task1 = _mock_task(id=1, user_id=1)
        task2 = _mock_task(id=2, user_id=1)
        dep_mock = MagicMock()
        dep_mock.id = 10
        dep_mock.task_id = 1
        dep_mock.prerequisite_task_id = 2
        dep_mock.created_at = datetime.now(timezone.utc)

        async def mock_get_task(db, tid):
            if tid == 1:
                return task1
            elif tid == 2:
                return task2
            return None

        with patch("app.api.v1.tasks.get_task_by_id", side_effect=mock_get_task):
            with patch("app.api.v1.tasks.add_task_dependency", new_callable=AsyncMock, return_value=dep_mock):
                response = await authenticated_client.post(
                    "/api/v1/tasks/1/dependencies",
                    json={"prerequisite_task_id": 2}
                )
        assert response.status_code == 201
        assert response.json()["task_id"] == 1
        assert response.json()["prerequisite_task_id"] == 2

    @pytest.mark.asyncio
    async def test_list_dependencies_endpoint(self, authenticated_client):
        """GET /tasks/{id}/dependencies returns list of dependencies."""
        task = _mock_task(id=1, user_id=1)
        dep_mock = MagicMock()
        dep_mock.id = 10
        dep_mock.task_id = 1
        dep_mock.prerequisite_task_id = 2
        dep_mock.created_at = datetime.now(timezone.utc)

        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            with patch("app.api.v1.tasks.get_task_dependencies", new_callable=AsyncMock, return_value=[dep_mock]):
                response = await authenticated_client.get("/api/v1/tasks/1/dependencies")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["prerequisite_task_id"] == 2

    @pytest.mark.asyncio
    async def test_remove_dependency_endpoint(self, authenticated_client):
        """DELETE /tasks/{id}/dependencies/{prereq_id} removes dependency."""
        task = _mock_task(id=1, user_id=1)
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            with patch("app.api.v1.tasks.remove_task_dependency", new_callable=AsyncMock, return_value=True):
                response = await authenticated_client.delete("/api/v1/tasks/1/dependencies/2")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_get_overdue_tasks(self, authenticated_client):
        """GET /tasks/overdue should return overdue tasks."""
        overdue_task = _mock_task(id=10, user_id=1, status=TaskStatus.TODO)
        with patch("app.api.v1.tasks.get_overdue_tasks_for_user", new_callable=AsyncMock, return_value=[overdue_task]):
            response = await authenticated_client.get("/api/v1/tasks/overdue")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 10

    @pytest.mark.asyncio
    async def test_get_today_summary(self, authenticated_client):
        """GET /tasks/summary/today should return today's metrics and daily objective."""
        t1 = _mock_task(id=1, user_id=1, status=TaskStatus.COMPLETED)
        t2 = _mock_task(id=2, user_id=1, status=TaskStatus.IN_PROGRESS)
        with patch("app.api.v1.tasks.get_user_tasks_for_day", new_callable=AsyncMock, return_value=[t1, t2]):
            with patch("app.api.v1.tasks.get_overdue_tasks_for_user", new_callable=AsyncMock, return_value=[]):
                response = await authenticated_client.get("/api/v1/tasks/summary/today")
        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 2
        assert data["completed_tasks"] == 1
        assert data["in_progress_tasks"] == 1
        assert data["completion_percentage"] == 50.0
        assert data["daily_objective"] is not None

    @pytest.mark.asyncio
    async def test_get_task_detail_endpoint(self, authenticated_client):
        """GET /tasks/{task_id} should return task detail."""
        task = _mock_task(id=1, user_id=1)
        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            response = await authenticated_client.get("/api/v1/tasks/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["topic"]["name"] == "Subnetting"

    @pytest.mark.asyncio
    async def test_task_completion_workflow_with_confidence_and_hours(self, authenticated_client):
        """PATCH /tasks/{id} should update status to completed, confidence score, and hours."""
        task = _mock_task(id=1, user_id=1)
        updated = _mock_task(id=1, user_id=1, status=TaskStatus.COMPLETED)
        updated.confidence_score = 90
        updated.actual_hours = 2.5
        updated.notes = "Understood CIDR calculations clearly."

        with patch("app.api.v1.tasks.get_task_by_id", new_callable=AsyncMock, return_value=task):
            with patch("app.api.v1.tasks.update_task", new_callable=AsyncMock, return_value=updated):
                response = await authenticated_client.patch(
                    "/api/v1/tasks/1",
                    json={
                        "status": "completed",
                        "confidence_score": 90,
                        "actual_hours": 2.5,
                        "notes": "Understood CIDR calculations clearly."
                    }
                )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["confidence_score"] == 90
        assert data["actual_hours"] == 2.5
        assert "CIDR" in data["notes"]


