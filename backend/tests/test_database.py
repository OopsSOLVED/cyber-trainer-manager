"""
Database infrastructure tests.

Tests for the database module — engine creation, session factory,
health check, Base model, and configuration.

These tests use mocking and do not require a live PostgreSQL instance.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone


# ── Configuration Tests ──────────────────────────────────────────

class TestDatabaseConfig:
    """Test database-related configuration."""

    def test_database_url_has_asyncpg_driver(self):
        """DATABASE_URL must use the asyncpg driver."""
        from app.core.config import settings
        assert "+asyncpg" in settings.DATABASE_URL

    def test_database_test_url_exists(self):
        """DATABASE_TEST_URL must be defined and different from DATABASE_URL."""
        from app.core.config import settings
        assert settings.DATABASE_TEST_URL is not None
        assert len(settings.DATABASE_TEST_URL) > 0

    def test_database_url_sync_removes_asyncpg(self):
        """database_url_sync should produce a URL without +asyncpg."""
        from app.core.config import settings
        sync_url = settings.database_url_sync
        assert "+asyncpg" not in sync_url


# ── Engine Tests ─────────────────────────────────────────────────

class TestEngine:
    """Test the SQLAlchemy engine configuration."""

    def test_engine_is_created(self):
        """The async engine should be created at module import."""
        from app.core.database import engine
        assert engine is not None

    def test_engine_url_matches_config(self):
        """Engine URL should have the correct driver, host, and database."""
        from app.core.database import engine
        url = engine.url
        assert url.drivername == "postgresql+asyncpg"
        assert url.host == "localhost"
        assert url.database == "cyber_trainer"

    def test_session_factory_is_created(self):
        """The async session factory should be created at module import."""
        from app.core.database import async_session_factory
        assert async_session_factory is not None


# ── Base Model Tests ─────────────────────────────────────────────

class TestBaseModel:
    """Test the declarative Base model."""

    def test_base_has_metadata(self):
        """Base should have MetaData with naming conventions."""
        from app.models.base import Base
        assert Base.metadata is not None
        assert Base.metadata.naming_convention is not None

    def test_naming_convention_keys(self):
        """Naming convention should include ix, uq, ck, fk, pk."""
        from app.models.base import Base
        nc = Base.metadata.naming_convention
        for key in ["ix", "uq", "ck", "fk", "pk"]:
            assert key in nc, f"Missing naming convention key: {key}"

    def test_base_has_common_columns(self):
        """Base should define id, created_at, updated_at columns."""
        from app.models.base import Base
        import inspect
        # Check that the class has the mapped attributes
        annotations = {}
        for cls in inspect.getmro(Base):
            if hasattr(cls, "__annotations__"):
                annotations.update(cls.__annotations__)
        assert "id" in annotations
        assert "created_at" in annotations
        assert "updated_at" in annotations


# ── Health Check Tests ───────────────────────────────────────────

class TestDatabaseHealthCheck:
    """Test the database health check function."""

    @pytest.mark.asyncio
    async def test_check_db_health_returns_true_on_success(self):
        """check_db_health should return True when DB is reachable."""
        with patch("app.core.database.engine") as mock_engine:
            mock_conn = AsyncMock()
            mock_conn.execute = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_engine.begin.return_value = mock_ctx

            from app.core.database import check_db_health
            result = await check_db_health()
            assert result is True

    @pytest.mark.asyncio
    async def test_check_db_health_returns_false_on_failure(self):
        """check_db_health should return False when DB is unreachable."""
        with patch("app.core.database.engine") as mock_engine:
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(side_effect=ConnectionError("Connection refused"))
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_engine.begin.return_value = mock_ctx

            from app.core.database import check_db_health
            result = await check_db_health()
            assert result is False


# ── Init/Close Tests ─────────────────────────────────────────────

class TestDatabaseLifecycle:
    """Test database init and close functions."""

    @pytest.mark.asyncio
    async def test_init_db_calls_select_1(self):
        """init_db should execute SELECT 1 to verify connectivity."""
        with patch("app.core.database.engine") as mock_engine:
            mock_conn = AsyncMock()
            mock_conn.execute = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_engine.begin.return_value = mock_ctx

            from app.core.database import init_db
            await init_db()
            mock_conn.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_db_disposes_engine(self):
        """close_db should dispose the engine's connection pool."""
        with patch("app.core.database.engine") as mock_engine:
            mock_engine.dispose = AsyncMock()

            from app.core.database import close_db
            await close_db()
            mock_engine.dispose.assert_called_once()

    @pytest.mark.asyncio
    async def test_init_db_raises_on_connection_failure(self):
        """init_db should raise when database is unreachable."""
        with patch("app.core.database.engine") as mock_engine:
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(side_effect=ConnectionError("Connection refused"))
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_engine.begin.return_value = mock_ctx

            from app.core.database import init_db
            with pytest.raises(ConnectionError):
                await init_db()


# ── Session Dependency Tests ─────────────────────────────────────

class TestGetDbDependency:
    """Test the get_db FastAPI dependency."""

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """get_db should yield an AsyncSession-like object."""
        with patch("app.core.database.async_session_factory") as mock_factory:
            mock_session = AsyncMock()
            mock_session.commit = AsyncMock()
            mock_session.rollback = AsyncMock()
            mock_session.close = AsyncMock()

            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_factory.return_value = mock_ctx

            from app.core.database import get_db
            async for session in get_db():
                assert session is mock_session
