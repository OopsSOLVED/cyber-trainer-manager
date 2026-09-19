"""initial_schema_base_model

Revision ID: f51990060930
Revises: 
Create Date: 2026-09-19 07:53:07.215545

Initial migration establishing the Alembic version tracking.
The Base model provides common columns (id, created_at, updated_at)
but is not itself a concrete table. Concrete model tables will be
created in subsequent migrations starting with Session 3 (User model).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f51990060930'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema — no tables yet (Base is abstract)."""
    pass


def downgrade() -> None:
    """Downgrade schema — no tables to remove."""
    pass
