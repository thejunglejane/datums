"""Rename snapshot tables to report tables.

Revision ID: c984c6d45f23
Revises: 
Create Date: 2016-01-25 22:42:52.440714

"""

# revision identifiers, used by Alembic.
revision = 'c984c6d45f23'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('snapshots', 'reports')
    op.rename_table('audio_snapshots', 'audio_reports')
    op.rename_table('location_snapshots', 'location_reports')
    op.rename_table('placemark_snapshots', 'placemark_reports')
    op.rename_table('weather_snapshots', 'weather_reports')


def downgrade():
    op.rename_table('reports', 'snapshots')
    op.rename_table('audio_reports', 'audio_snapshots')
    op.rename_table('location_reports', 'location_snapshots')
    op.rename_table('placemark_reports', 'placemark_snapshots')
    op.rename_table('weather_reports', 'weather_snapshots')
