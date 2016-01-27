"""Add foreign key constraints

Revision ID: 457bbf802239
Revises: e912ea8b3cb1
Create Date: 2016-01-25 23:04:37.492418

"""

# revision identifiers, used by Alembic.
revision = '457bbf802239'
down_revision = 'e912ea8b3cb1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_foreign_key(
        constraint_name='audio_reports_report_id_fkey',
        source_table='audio_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='location_reports_report_id_fkey',
        source_table='location_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='placemark_reports_location_report_id_fkey',
        source_table='placemark_reports', referent_table='location_reports',
        local_cols=['location_report_id'], remote_cols=['id'],
        ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='weather_reports_report_id_fkey',
        source_table='weather_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='responses_report_id_fkey',
        source_table='responses', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('audio_reports') as batch_op:
        batch_op.drop_constraint('audio_reports_report_id_fkey')

    with op.batch_alter_table('location_reports') as batch_op:
        batch_op.drop_constraint('location_reports_report_id_fkey')

    with op.batch_alter_table('placemark_reports') as batch_op:
        batch_op.drop_constraint('placemark_reports_location_report_id_fkey')

    with op.batch_alter_table('weather_reports') as batch_op:
        batch_op.drop_constraint('weather_reports_report_id_fkey')

    with op.batch_alter_table('responses') as batch_op:
        batch_op.drop_constraint('responses_report_id_fkey')
