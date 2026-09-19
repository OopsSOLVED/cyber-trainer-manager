"""
Authentication endpoints.

Handles user registration, login, and profile retrieval.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.repositories.user import get_user_by_email, create_user, update_last_login
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth import hash_password, verify_password, create_access_token
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with email, password, and display name.",
)
async def register(
    body: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.

    - Validates email uniqueness
    - Hashes password with bcrypt
    - Returns the created user profile (no password)
    """
    existing = await get_user_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed = hash_password(body.password)
    user = await create_user(
        db=db,
        email=body.email,
        hashed_password=hashed,
        display_name=body.display_name,
    )

    logger.info("User registered: %s", body.email)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get access token",
    description="Authenticates with email/password and returns a JWT access token.",
)
async def login(
    body: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user and return JWT token.

    - Verifies email exists
    - Verifies password against bcrypt hash
    - Updates last_login_at timestamp
    - Returns JWT access token
    """
    user = await get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    await update_last_login(db, user)
    token = create_access_token(subject=str(user.id))
    logger.info("User logged in: %s", user.email)
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile information.",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user's profile.

    Requires a valid JWT token in the Authorization header.
    """
    return current_user
