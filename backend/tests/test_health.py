"""
Health endpoint tests.

Verifies the liveness and readiness probes return correct
status codes, fields, and values.
"""

import pytest


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


@pytest.mark.asyncio
async def test_readiness_returns_200(client):
    """Readiness endpoint should return HTTP 200."""
    response = await client.get("/api/v1/health/readiness")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_readiness_returns_ready_status(client):
    """Readiness endpoint should report 'ready' when all checks pass."""
    response = await client.get("/api/v1/health/readiness")
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_readiness_contains_checks(client):
    """Readiness response must contain a 'checks' object."""
    response = await client.get("/api/v1/health/readiness")
    data = response.json()
    assert "checks" in data
    assert isinstance(data["checks"], dict)
    assert data["checks"]["application"] is True


@pytest.mark.asyncio
async def test_readiness_contains_required_fields(client):
    """Readiness response must contain status, version, timestamp, checks."""
    response = await client.get("/api/v1/health/readiness")
    data = response.json()
    required_fields = ["status", "version", "timestamp", "checks"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
