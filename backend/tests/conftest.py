"""
Test configuration and shared fixtures.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """
    Async HTTP test client for the FastAPI application.

    Uses httpx AsyncClient with ASGITransport to test
    the application without starting a real server.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
