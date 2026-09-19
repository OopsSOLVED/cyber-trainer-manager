"""
Test configuration and shared fixtures.

Provides:
- Async HTTP test client (no database required)
- Database-aware test client (requires PostgreSQL)
- Test database session fixture
"""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.core.config import settings


@pytest.fixture
def app():
    """
    Create a fresh FastAPI application instance for testing.

    Does NOT trigger lifespan (no database connection).
    Use this for tests that don't need a database.
    """
    return create_app()


@pytest.fixture
async def client(app):
    """
    Async HTTP test client for the FastAPI application.

    Uses httpx AsyncClient with ASGITransport to test
    the application without starting a real server.

    Database lifecycle is NOT triggered — use this for
    API tests that mock database calls or don't need a DB.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
async def client_with_db_mock(app):
    """
    Async HTTP test client with database health check mocked.

    Simulates a healthy database without requiring PostgreSQL.
    Used for health/readiness endpoint tests.
    """
    with patch("app.api.v1.health.check_db_health", new_callable=AsyncMock, return_value=True):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac


@pytest.fixture
async def client_with_db_down_mock(app):
    """
    Async HTTP test client with database health check mocked as DOWN.

    Simulates an unreachable database. Used for testing degraded
    readiness status.
    """
    with patch("app.api.v1.health.check_db_health", new_callable=AsyncMock, return_value=False):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
