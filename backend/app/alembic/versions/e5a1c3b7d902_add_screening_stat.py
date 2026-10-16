"""add screening_stat

Revision ID: e5a1c3b7d902
Revises: d3f8a1c5e7b2
Create Date: 2026-10-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a1c3b7d902'
down_revision = 'd3f8a1c5e7b2'
branch_labels = None
depends_on = None


def upgrade():
    # Statistics without direct identity: no user id, IP, created_at, exact age,
    # raw vitals, or drug text. See app/domain/screening_stat.py.
    op.create_table(
        'screening_stat',
        sa.Column('event_id', sa.Uuid(), nullable=False),
        sa.Column('day', sa.Date(), nullable=False),
        sa.Column('flow_id', sa.String(length=20), nullable=False),
        sa.Column('route', sa.String(length=10), nullable=False),
        sa.Column('unknown', sa.Boolean(), nullable=False),
        sa.Column('top_disease', sa.String(length=20), nullable=True),
        sa.Column('top_score', sa.Float(), nullable=True),
        sa.Column('others', sa.JSON(), nullable=False),
        sa.Column('engine', sa.String(length=20), nullable=False),
        sa.Column('who', sa.String(length=30), nullable=True),
        sa.Column('sex', sa.String(length=1), nullable=True),
        sa.Column('age_band', sa.String(length=5), nullable=True),
        sa.Column('pregnant', sa.Boolean(), nullable=True),
        sa.Column('province', sa.String(length=64), nullable=True),
        sa.Column('complaint', sa.String(length=30), nullable=True),
        sa.Column('pattern', sa.String(length=30), nullable=True),
        sa.Column('red_flags', sa.JSON(), nullable=False),
        sa.Column('companion', sa.JSON(), nullable=False),
        sa.Column('eco', sa.JSON(), nullable=False),
        sa.Column('body', sa.JSON(), nullable=False),
        sa.Column('vital_proxy', sa.JSON(), nullable=False),
        sa.Column('nutrition_proxy', sa.String(length=10), nullable=True),
        sa.Column('pain', sa.Integer(), nullable=True),
        sa.Column('temp_cat', sa.String(length=15), nullable=True),
        sa.Column('bp_cat', sa.String(length=15), nullable=True),
        sa.Column('glucose_high', sa.Boolean(), nullable=False),
        sa.Column('bmi_cat', sa.String(length=10), nullable=True),
        sa.Column('no_thermo', sa.Boolean(), nullable=False),
        sa.Column('no_bp', sa.Boolean(), nullable=False),
        sa.Column('drugs_given', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('event_id'),
    )
    op.create_index(op.f('ix_screening_stat_day'), 'screening_stat', ['day'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_screening_stat_day'), table_name='screening_stat')
    op.drop_table('screening_stat')
