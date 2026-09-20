"""add_task_dependencies_and_fields

Revision ID: d5e6f7g8h9i0
Revises: c4d5e6f7g8h9
Create Date: 2026-09-20

Adds priority, task_type, due_date, confidence_score, and review_date columns
to the tasks table, and creates the task_dependencies table.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e6f7g8h9i0'
down_revision: Union[str, Sequence[str], None] = 'c4d5e6f7g8h9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Add columns to tasks ──────────────────────────────────────
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), nullable=False, server_default='medium'))
    op.add_column('tasks', sa.Column('task_type', sa.String(length=30), nullable=False, server_default='study'))
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tasks', sa.Column('confidence_score', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('review_date', sa.DateTime(timezone=True), nullable=True))

    # ── Create task_dependencies table ────────────────────────────
    op.create_table(
        'task_dependencies',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('prerequisite_task_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_task_dependencies'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_dependencies_task_id_tasks', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['prerequisite_task_id'], ['tasks.id'], name='fk_task_dependencies_prereq_id_tasks', ondelete='CASCADE'),
        sa.UniqueConstraint('task_id', 'prerequisite_task_id', name='uq_task_prerequisite')
    )
    op.create_index('ix_task_dependencies_id', 'task_dependencies', ['id'])
    op.create_index('ix_task_dependencies_task_id', 'task_dependencies', ['task_id'])


def downgrade() -> None:
    op.drop_table('task_dependencies')
    op.drop_column('tasks', 'review_date')
    op.drop_column('tasks', 'confidence_score')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'task_type')
    op.drop_column('tasks', 'priority')
