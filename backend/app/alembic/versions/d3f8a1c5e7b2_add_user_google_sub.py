"""add user google_sub

Revision ID: d3f8a1c5e7b2
Revises: b7d2e4f19a6c
Create Date: 2026-10-15 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f8a1c5e7b2'
down_revision = 'b7d2e4f19a6c'
branch_labels = None
depends_on = None


def upgrade():
    # Google "sub" of the linked account; null = never linked to Google.
    op.add_column(
        'user', sa.Column('google_sub', sa.String(length=255), nullable=True)
    )
    op.create_index(
        op.f('ix_user_google_sub'), 'user', ['google_sub'], unique=True
    )


def downgrade():
    op.drop_index(op.f('ix_user_google_sub'), table_name='user')
    op.drop_column('user', 'google_sub')
