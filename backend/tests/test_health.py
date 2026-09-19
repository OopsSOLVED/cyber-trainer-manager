"""
Health endpoint tests.

Verifies the liveness and readiness probes return correct
status codes, fields, and values.

Uses mocked database fixtures so tests run without PostgreSQL.
"""

import pytest


# ── Liveness Probe Tests ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_returns_200(client):
    """Health endpoint should return HTTP 200."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_returns_healthy_status(client):
    """Health endpoint should report 'healthy' status."""
    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_contains_required_fields(client):
    """Health response must contain status, version, timestamp, application."""
    response = await client.get("/api/v1/health")
    data = response.json()
    required_fields = ["status", "version", "timestamp", "application", "environment"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


@pytest.mark.asyncio
async def test_health_version_matches_config(client):
    """Health version must match the configured app version."""
    from app.core.config import settings

    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["version"] == settings.APP_VERSION


@pytest.mark.asyncio
async def test_health_timestamp_is_iso_format(client):
    """Health timestamp must be a valid ISO 8601 string."""
    from datetime import datetime

    response = await client.get("/api/v1/health")
    data = response.json()
    # Should not raise ValueError
    datetime.fromisoformat(data["timestamp"])


# ── Readiness Probe Tests (Database Healthy) ─────────────────────

@pytest.mark.asyncio
async def test_readiness_returns_200(client_with_db_mock):
    """Readiness endpoint should return HTTP 200."""
    response = await client_with_db_mock.get("/api/v1/health/readiness")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_readiness_returns_ready_when_db_healthy(client_with_db_mock):
    """Readiness endpoint should report 'ready' when database is healthy."""
    response = await client_with_db_mock.get("/api/v1/health/readiness")
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_readiness_contains_checks(client_with_db_mock):
    """Readiness response must contain a 'checks' object with app and db."""
    response = await client_with_db_mock.get("/api/v1/health/readiness")
    data = response.json()
    assert "checks" in data
    assert isinstance(data["checks"], dict)
    assert data["checks"]["application"] is True
    assert data["checks"]["database"] is True


@pytest.mark.asyncio
async def test_readiness_contains_required_fields(client_with_db_mock):
    """Readiness response must contain status, version, timestamp, checks."""
    response = await client_with_db_mock.get("/api/v1/health/readiness")
    data = response.json()
    required_fields = ["status", "version", "timestamp", "checks"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


# ── Readiness Probe Tests (Database Down) ────────────────────────

@pytest.mark.asyncio
async def test_readiness_returns_degraded_when_db_down(client_with_db_down_mock):
    """Readiness should report 'degraded' when database is unreachable."""
    response = await client_with_db_down_mock.get("/api/v1/health/readiness")
    data = response.json()
    assert data["status"] == "degraded"


@pytest.mark.asyncio
async def test_readiness_shows_db_false_when_down(client_with_db_down_mock):
    """Readiness checks should show database=false when DB is unreachable."""
    response = await client_with_db_down_mock.get("/api/v1/health/readiness")
    data = response.json()
    assert data["checks"]["database"] is False
    assert data["checks"]["application"] is True
