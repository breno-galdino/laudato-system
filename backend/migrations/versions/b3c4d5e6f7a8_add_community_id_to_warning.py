"""add community_id to warning

Revision ID: b3c4d5e6f7a8
Revises: 74ad24c0f7d8
Create Date: 2026-05-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'b3c4d5e6f7a8'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('warning', sa.Column('community_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_warning_community_id'), 'warning', ['community_id'], unique=False)
    op.create_foreign_key(None, 'warning', 'community', ['community_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'warning', type_='foreignkey')
    op.drop_index(op.f('ix_warning_community_id'), table_name='warning')
    op.drop_column('warning', 'community_id')
