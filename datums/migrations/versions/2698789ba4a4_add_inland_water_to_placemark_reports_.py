"""Add inland_water to placemark_reports table

Revision ID: 2698789ba4a4
Revises: 8f22f932fa58
Create Date: 2016-01-25 23:11:18.515616

"""

# revision identifiers, used by Alembic.
revision = '2698789ba4a4'
down_revision = '8f22f932fa58'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, String


def upgrade():
    op.add_column('placemark_reports', Column('inland_water', String))


def downgrade():
    op.drop_column('placemark_reports', 'inland_water')
