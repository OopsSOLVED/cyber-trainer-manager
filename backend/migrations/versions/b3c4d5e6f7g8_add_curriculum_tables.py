"""add_curriculum_tables

Revision ID: b3c4d5e6f7g8
Revises: a2b3c4d5e6f7
Create Date: 2026-09-19

Creates the curriculum hierarchy tables:
phases → skill_layers → domains → topics → learning_objectives
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b3c4d5e6f7g8'
down_revision: Union[str, Sequence[str], None] = 'a2b3c4d5e6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create curriculum tables."""

    # ── Phases ───────────────────────────────────────────────
    op.create_table(
        'phases',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_phases'),
        sa.UniqueConstraint('name', name='uq_phases_name'),
    )
    op.create_index('ix_phases_id', 'phases', ['id'])

    # ── Skill Layers ─────────────────────────────────────────
    op.create_table(
        'skill_layers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_skill_layers'),
        sa.ForeignKeyConstraint(['phase_id'], ['phases.id'], name='fk_skill_layers_phase_id_phases', ondelete='CASCADE'),
    )
    op.create_index('ix_skill_layers_id', 'skill_layers', ['id'])

    # ── Domains ──────────────────────────────────────────────
    op.create_table(
        'domains',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('skill_layer_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_domains'),
        sa.ForeignKeyConstraint(['skill_layer_id'], ['skill_layers.id'], name='fk_domains_skill_layer_id_skill_layers', ondelete='CASCADE'),
    )
    op.create_index('ix_domains_id', 'domains', ['id'])

    # ── Topics ───────────────────────────────────────────────
    op.create_table(
        'topics',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('domain_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('day_number', sa.Integer(), nullable=True, comment='Which day in the 196-day plan'),
        sa.Column('estimated_hours', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('difficulty', sa.String(20), nullable=False, server_default="'intermediate'"),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_topics'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], name='fk_topics_domain_id_domains', ondelete='CASCADE'),
    )
    op.create_index('ix_topics_id', 'topics', ['id'])
    op.create_index('ix_topics_day_number', 'topics', ['day_number'])

    # ── Learning Objectives ──────────────────────────────────
    op.create_table(
        'learning_objectives',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_measurable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id', name='pk_learning_objectives'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], name='fk_learning_objectives_topic_id_topics', ondelete='CASCADE'),
    )
    op.create_index('ix_learning_objectives_id', 'learning_objectives', ['id'])


def downgrade() -> None:
    """Drop curriculum tables in reverse order."""
    op.drop_table('learning_objectives')
    op.drop_table('topics')
    op.drop_table('domains')
    op.drop_table('skill_layers')
    op.drop_table('phases')
