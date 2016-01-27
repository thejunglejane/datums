"""Rename snapshot_id columns to report_id

Revision ID: e912ea8b3cb1
Revises: 728b24c64cea
Create Date: 2016-01-25 23:04:18.091843

"""

# revision identifiers, used by Alembic.
revision = 'e912ea8b3cb1'
down_revision = '728b24c64cea'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'audio_reports', 'snapshot_id', new_column_name='report_id')

    op.alter_column(
        'location_reports', 'snapshot_id', new_column_name='report_id')

    op.alter_column(
        'placemark_reports', 'location_snapshot_id',
        new_column_name='location_report_id')

    op.alter_column(
        'weather_reports', 'snapshot_id', new_column_name='report_id')

    op.alter_column('responses', 'snapshot_id', new_column_name='report_id')


def downgrade():
    op.alter_column(
        'audio_reports', 'report_id', new_column_name='snapshot_id')

    op.alter_column(
        'location_reports', 'report_id', new_column_name='snapshot_id')

    op.alter_column(
        'placemark_reports', 'report_id', new_column_name='snapshot_id')

    op.alter_column(
        'weather_reports', 'report_id', new_column_name='snapshot_id')

    op.alter_column('responses', 'report_id', new_column_name='snapshot_id')
