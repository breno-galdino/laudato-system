"""rebuild community table with multi-tenancy and type fields

Revision ID: a1b2c3d4e5f6
Revises: d365940dc964
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'd365940dc964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('community')

    op.create_table(
        'community',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('parish_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('type', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='grupo'),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
        sa.Column('address', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=True),
        sa.Column('coordinator', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
        sa.Column('meeting_day', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
        sa.Column('meeting_time', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['parish_id'], ['parish.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_community_parish_id', 'community', ['parish_id'])


def downgrade() -> None:
    op.drop_index('ix_community_parish_id', table_name='community')
    op.drop_table('community')

    op.create_table(
        'community',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('adress', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
