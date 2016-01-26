"""Add altitude_reports table

Revision ID: f24937651f71
Revises: 457bbf802239
Create Date: 2016-01-25 23:07:52.202616

"""

# revision identifiers, used by Alembic.
revision = 'f24937651f71'
down_revision = '457bbf802239'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'altitude_reports',
        Column('id', UUIDType, primary_key=True),
        Column('floors_ascended', Numeric),
        Column('floors_descended', Numeric),
        Column('gps_altitude_from_location', Numeric),
        Column('gps_altitude_raw', Numeric),
        Column('pressure', Numeric),
        Column('pressure_adjusted', Numeric),
        Column('report_id', UUIDType, ForeignKey(
            'reports.id', ondelete='CASCADE'), nullable=False))


def downgrade():
    op.drop_table('altitude_reports')
