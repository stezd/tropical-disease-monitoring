"""add facility wa_number

Revision ID: c4a7e9f12b30
Revises: 70e8d04328f1
Create Date: 2026-10-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'c4a7e9f12b30'
down_revision = '70e8d04328f1'
branch_labels = None
depends_on = None


def upgrade():
    # Curated WhatsApp number, never written by the MSI sync.
    op.add_column(
        'facility',
        sa.Column('wa_number', sqlmodel.sql.sqltypes.AutoString(length=32), nullable=True),
    )


def downgrade():
    op.drop_column('facility', 'wa_number')
