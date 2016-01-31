"""Add primary key constraints

Revision ID: 728b24c64cea
Revises: 785ab1c2c255
Create Date: 2016-01-25 22:54:18.023243

"""

# revision identifiers, used by Alembic.
revision = '728b24c64cea'
down_revision = '785ab1c2c255'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('audio_reports') as batch_op:
        batch_op.drop_constraint('audio_snapshots_pkey')
        batch_op.create_primary_key('audio_reports_pkey', columns=['id'])

    with op.batch_alter_table('location_reports') as batch_op:
        batch_op.drop_constraint('location_snapshots_pkey')
        batch_op.create_primary_key('location_reports_pkey', columns=['id'])

    with op.batch_alter_table('placemark_reports') as batch_op:
        batch_op.drop_constraint('placemark_snapshots_pkey')
        batch_op.create_primary_key('placemark_reports_pkey', columns=['id'])

    with op.batch_alter_table('weather_reports') as batch_op:
        batch_op.drop_constraint('weather_snapshots_pkey')
        batch_op.create_primary_key('weather_reports_pkey', columns=['id'])


def downgrade():
    with op.batch_alter_table('audio_reports') as batch_op:
        batch_op.drop_constraint('audio_reports_pkey')
        batch_op.create_primary_key('audio_snapshots_pkey', columns=['id'])

    with op.batch_alter_table('location_reports') as batch_op:
        batch_op.drop_constraint('location_reports_pkey')
        batch_op.create_primary_key('location_snapshots_pkey', columns=['id'])

    with op.batch_alter_table('placemark_reports') as batch_op:
        batch_op.drop_constraint('placemark_reports_pkey')
        batch_op.create_primary_key('placemark_snapshots_pkey', columns=['id'])

    with op.batch_alter_table('weather_reports') as batch_op:
        batch_op.drop_constraint('weather_reports_pkey')
        batch_op.create_primary_key('weather_snapshots_pkey', columns=['id'])

