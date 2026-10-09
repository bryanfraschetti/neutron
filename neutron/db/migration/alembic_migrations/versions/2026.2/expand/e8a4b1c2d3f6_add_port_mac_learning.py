from alembic import op
import sqlalchemy as sa


revision = 'e8a4b1c2d3f6'
down_revision = 'c7f8d9e0f1a2'


def upgrade():
    op.create_table(
        'port_mac_learning',
        sa.Column('port_id', sa.String(length=36),
                  sa.ForeignKey('ports.id', ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('mac_learning_enabled', sa.Boolean(), nullable=False,
                  server_default=sa.false()))
