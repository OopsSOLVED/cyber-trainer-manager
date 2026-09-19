"""
Base model for all SQLAlchemy ORM models.

Provides common columns (id, created_at, updated_at) and naming
conventions. All application models should inherit from Base.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ── Naming Convention ────────────────────────────────────────────
# Consistent constraint naming makes Alembic auto-migrations reliable.
# See: https://alembic.sqlalchemy.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    Provides:
    - Consistent table naming convention
    - Common columns: id, created_at, updated_at
    - MetaData with naming conventions for Alembic
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    # ── Common Columns ───────────────────────────────────────────
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
