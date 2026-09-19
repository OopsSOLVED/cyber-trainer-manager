"""add_task_tables

Revision ID: c4d5e6f7g8h9
Revises: b3c4d5e6f7g8
Create Date: 2026-09-19

Creates the tasks and subtasks tables with the task_status enum.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c4d5e6f7g8h9'
down_revision: Union[str, Sequence[str], None] = 'b3c4d5e6f7g8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks and subtasks tables."""
    # Ensure a clean slate if migration failed previously
    op.execute("DROP TYPE IF EXISTS task_status CASCADE;")

    # ── Tasks ───────────────────────────────────────────────
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('TODO', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED', 'SKIPPED', name='task_status', create_constraint=True), nullable=False, server_default='TODO'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('estimated_hours', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('actual_hours', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('assigned_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_tasks'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], name='fk_tasks_topic_id_topics', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_tasks_user_id_users', ondelete='CASCADE')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'])
    op.create_index('ix_tasks_user_id_assigned_date', 'tasks', ['user_id', 'assigned_date'])

    # ── Subtasks ───────────────────────────────────────────────
    op.create_table(
        'subtasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('learning_objective_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('TODO', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED', 'SKIPPED', name='task_status', create_constraint=True), nullable=False, server_default='TODO'),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_subtasks'),
        sa.ForeignKeyConstraint(['learning_objective_id'], ['learning_objectives.id'], name='fk_subtasks_learning_objective_id_learning_objectives', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_subtasks_task_id_tasks', ondelete='CASCADE')
    )
    op.create_index('ix_subtasks_id', 'subtasks', ['id'])


def downgrade() -> None:
    """Drop tasks and subtasks tables."""
    op.drop_table('subtasks')
    op.drop_table('tasks')
    task_status = postgresql.ENUM('TODO', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED', 'SKIPPED', name='task_status')
    task_status.drop(op.get_bind(), checkfirst=True)
