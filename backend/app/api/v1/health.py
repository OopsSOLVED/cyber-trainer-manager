"""
Health check endpoints.

Provides liveness and readiness probes for the application.
- /health — Basic liveness check (is the process running?)
- /health/readiness — Readiness check (are dependencies available?)
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import check_db_health

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    summary="Liveness probe",
    description="Returns application health status, version, and timestamp.",
    response_description="Health status object",
)
async def health_check():
    """
    Basic liveness probe.

    Returns 200 if the application process is running and able
    to handle HTTP requests. Does not verify external dependencies.
    """
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": "development" if settings.DEBUG else "production",
    }


@router.get(
    "/readiness",
    summary="Readiness probe",
    description="Returns readiness status including dependency checks.",
    response_description="Readiness status object with dependency details",
)
async def readiness_check():
    """
    Readiness probe that verifies external dependencies.

    Checks:
    - Application process (always true if responding)
    - PostgreSQL connectivity
    """
    db_healthy = await check_db_health()

    checks = {
        "application": True,
        "database": db_healthy,
        # Future: "redis": await check_redis_connection(),
    }

    all_ready = all(checks.values())

    return {
        "status": "ready" if all_ready else "degraded",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
