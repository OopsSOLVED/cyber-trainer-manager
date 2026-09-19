"""
User ORM model.

Represents registered users of the application. Handles
authentication data and profile information.
"""

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.models.base import Base


class User(Base):
    """
    User account model.

    Stores authentication credentials and profile data.
    Password is stored as a bcrypt hash, never plaintext.
    """

    __tablename__ = "users"

    # ── Authentication ───────────────────────────────────────────
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ── Profile ──────────────────────────────────────────────────
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
