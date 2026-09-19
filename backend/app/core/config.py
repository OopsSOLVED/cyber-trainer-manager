"""
Application configuration using Pydantic Settings.

Reads from environment variables and .env file.
All application-wide settings are centralized here.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    For local development, create a .env file from .env.example.
    In production, set environment variables directly.
    """

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "Cybersecurity Trainer Task Manager"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str = Field(
        default="change-me-in-production",
        description="Secret key for signing tokens. Must be changed in production.",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="JWT access token expiration in minutes.",
    )

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/cyber_trainer",
        description="PostgreSQL connection string (async driver).",
    )

    DATABASE_TEST_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/cyber_trainer_test",
        description="PostgreSQL connection string for tests. Separate DB to avoid data conflicts.",
    )

    # ── Redis (future sessions) ──────────────────────────────────
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string for caching and background jobs.",
    )

    # ── CORS ─────────────────────────────────────────────────────
    CORS_ORIGINS: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins.",
    )

    # ── API ──────────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    from pydantic import model_validator
    
    @model_validator(mode='after')
    def fix_database_url(self) -> 'Settings':
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
        elif self.DATABASE_URL and self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self

    @property
    def database_url_sync(self) -> str:
        """Return a synchronous database URL for Alembic migrations."""
        return self.DATABASE_URL.replace("+asyncpg", "").replace(
            "postgresql", "postgresql"
        )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


# Singleton settings instance
settings = Settings()
