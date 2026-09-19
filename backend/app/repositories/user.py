"""
User repository.

Data access layer for User model operations.
All database queries for users are centralized here.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

logger = logging.getLogger(__name__)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch a user by email address. Returns None if not found."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Fetch a user by ID. Returns None if not found."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    email: str,
    hashed_password: str,
    display_name: str,
) -> User:
    """
    Create a new user record.

    Args:
        db: Database session.
        email: Unique email address.
        hashed_password: Bcrypt-hashed password.
        display_name: User's display name.

    Returns:
        The newly created User instance.
    """
    user = User(
        email=email,
        hashed_password=hashed_password,
        display_name=display_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    logger.info("Created user: %s (id=%s)", email, user.id)
    return user


async def update_last_login(db: AsyncSession, user: User) -> None:
    """Update the user's last_login_at timestamp."""
    user.last_login_at = datetime.now(timezone.utc)
    await db.flush()
