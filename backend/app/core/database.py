"""
Database engine, session, and connection management.

Provides async SQLAlchemy engine and session factory for the application.
All database access should go through the session dependency provided here.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Engine ───────────────────────────────────────────────────────
# The engine is created once at module level and shared across
# the application. It manages the connection pool.
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)

# ── Session Factory ──────────────────────────────────────────────
# Creates new AsyncSession instances. Each request gets its own session.
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Dependency ───────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.

    Usage in endpoints:
        @router.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            ...

    The session is automatically closed after the request completes.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Lifecycle ────────────────────────────────────────────────────
async def init_db() -> None:
    """
    Initialize database connection on application startup.

    Verifies connectivity by executing a simple query.
    Called from the application lifespan handler.
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established: %s", settings.DATABASE_URL.split("@")[-1])
    except Exception as e:
        logger.error("Failed to connect to database: %s", e)
        raise


async def close_db() -> None:
    """
    Close database connections on application shutdown.

    Disposes of the engine's connection pool.
    Called from the application lifespan handler.
    """
    await engine.dispose()
    logger.info("Database connections closed.")


async def check_db_health() -> bool:
    """
    Check database connectivity for health/readiness probes.

    Returns True if a simple query succeeds, False otherwise.
    Does not raise exceptions — used by the readiness endpoint.
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning("Database health check failed: %s", e)
        return False
