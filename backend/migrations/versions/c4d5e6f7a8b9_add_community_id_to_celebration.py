"""add community_id to celebration

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-05-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'c4d5e6f7a8b9'
down_revision: Union[str, None] = 'b3c4d5e6f7a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('celebration', sa.Column('community_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_celebration_community_id'), 'celebration', ['community_id'], unique=False)
    op.create_foreign_key(None, 'celebration', 'community', ['community_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'celebration', type_='foreignkey')
    op.drop_index(op.f('ix_celebration_community_id'), table_name='celebration')
    op.drop_column('celebration', 'community_id')
