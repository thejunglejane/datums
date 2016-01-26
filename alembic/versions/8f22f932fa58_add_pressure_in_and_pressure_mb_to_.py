"""Add pressure_in and pressure_mb to weather_reports table

Revision ID: 8f22f932fa58
Revises: f24937651f71
Create Date: 2016-01-25 23:09:20.325410

"""

# revision identifiers, used by Alembic.
revision = '8f22f932fa58'
down_revision = 'f24937651f71'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Numeric


def upgrade():
    op.add_column('weather_reports', Column('pressure_in', Numeric))
    op.add_column('weather_reports', Column('pressure_mb', Numeric))


def downgrade():
    op.drop_column('weather_reports', 'pressure_in')
    op.drop_column('weather_reports', 'pressure_mb')
