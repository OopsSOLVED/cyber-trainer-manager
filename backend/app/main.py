"""
Cybersecurity Trainer Task Manager — Main Application Entry Point.

This module creates and configures the FastAPI application instance,
including middleware, routers, and lifecycle management.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.health import router as health_router

# ── Logging Configuration ────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# ── Application Lifespan ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown.

    Startup:
    - Log application start
    - (Session 2+) Initialize database connection pool
    - (Future) Initialize Redis connection

    Shutdown:
    - (Session 2+) Close database connection pool
    - (Future) Close Redis connection
    """
    logger.info(
        "Starting %s v%s [%s]",
        settings.APP_NAME,
        settings.APP_VERSION,
        "development" if settings.DEBUG else "production",
    )
    # Session 2: await init_db()
    yield
    # Session 2: await close_db()
    logger.info("Application shutdown complete.")


# ── Application Factory ──────────────────────────────────────────
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "A production task-management and learning platform that turns "
            "the cybersecurity-trainer skill stack into a daily execution plan, "
            "tracks progress, and mirrors the live dashboard into Google Sheets."
        ),
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        openapi_url="/api/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ── CORS Middleware ──────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Register Routers ────────────────────────────────────────
    app.include_router(
        health_router,
        prefix=settings.API_V1_PREFIX,
    )

    # Session 3+: auth router
    # Session 4+: curriculum router
    # Session 5+: tasks router
    # ...

    logger.info(
        "Application configured with %d routes",
        len(app.routes),
    )

    return app


# ── Application Instance ─────────────────────────────────────────
app = create_app()
