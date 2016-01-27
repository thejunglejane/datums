"""Delete foreign key constraints

Revision ID: 785ab1c2c255
Revises: c984c6d45f23
Create Date: 2016-01-25 22:52:32.756368

"""

# revision identifiers, used by Alembic.
revision = '785ab1c2c255'
down_revision = 'c984c6d45f23'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('audio_reports') as batch_op:
        batch_op.drop_constraint(
            'audio_snapshots_snapshot_id_fkey')

    with op.batch_alter_table('location_reports') as batch_op:
        batch_op.drop_constraint(
            'location_snapshots_snapshot_id_fkey')

    with op.batch_alter_table('placemark_reports') as batch_op:
        batch_op.drop_constraint(
            'placemark_snapshots_location_snapshot_id_fkey')

    with op.batch_alter_table('weather_reports') as batch_op:
        batch_op.drop_constraint(
            'weather_snapshots_snapshot_id_fkey')

    with op.batch_alter_table('responses') as batch_op:
        batch_op.drop_constraint('responses_snapshot_id_fkey')


def downgrade():
    op.create_foreign_key(
        constraint_name='audio_snapshots_snapshot_id_fkey',
        source_table='audio_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='location_snapshots_snapshot_id_fkey',
        source_table='location_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='placemark_reports_snapshots_snapshot_id_fkey',
        source_table='placemark_reports', referent_table='location_reports',
        local_cols=['location_snapshot_id'], remote_cols=['id'],
        ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='weather_snapshots_snapshot_id_fkey',
        source_table='weather_reports', referent_table='reports',
        local_cols=['report_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_foreign_key(
        constraint_name='responses_snapshot_id_fkey', source_table='responses',
        referent_table='reports', local_cols=['report_id'],
        remote_cols=['id'], ondelete='CASCADE')
