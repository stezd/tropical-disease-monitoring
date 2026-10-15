"""add screening user_id

Revision ID: b7d2e4f19a6c
Revises: c4a7e9f12b30
Create Date: 2026-10-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d2e4f19a6c'
down_revision = 'c4a7e9f12b30'
branch_labels = None
depends_on = None


def upgrade():
    # Owner of a screening saved by a signed-in user. Existing rows stay anonymous.
    # Deleting the account deletes its screenings.
    op.add_column('screening', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.create_index(
        op.f('ix_screening_user_id'), 'screening', ['user_id'], unique=False
    )
    op.create_foreign_key(
        'screening_user_id_fkey',
        'screening',
        'user',
        ['user_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade():
    op.drop_constraint('screening_user_id_fkey', 'screening', type_='foreignkey')
    op.drop_index(op.f('ix_screening_user_id'), table_name='screening')
    op.drop_column('screening', 'user_id')
