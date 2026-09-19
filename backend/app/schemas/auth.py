"""
Authentication schemas.

Pydantic models for request/response validation in auth endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ──────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    """Registration request body."""
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be 8-128 characters.",
    )
    display_name: str = Field(
        min_length=1,
        max_length=100,
        description="Display name shown in the UI.",
    )


class UserLoginRequest(BaseModel):
    """Login request body."""
    email: EmailStr
    password: str


# ── Response Schemas ─────────────────────────────────────────────

class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user profile (returned by API)."""
    id: int
    email: str
    display_name: str
    is_active: bool
    created_at: datetime
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}
