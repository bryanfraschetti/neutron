from neutron_lib.db import constants as db_const
from neutron_lib.db import model_base
import sqlalchemy as sa
from sqlalchemy import orm

from neutron.db import models_v2


class PortMacLearning(model_base.BASEV2):
    __tablename__ = 'port_mac_learning'

    port_id = sa.Column(sa.String(db_const.UUID_FIELD_SIZE),
                        sa.ForeignKey('ports.id', ondelete='CASCADE'),
                        primary_key=True)
    mac_learning_enabled = sa.Column(sa.Boolean(), nullable=False,
                                     server_default=sa.false())
    port = orm.relationship(
        models_v2.Port, load_on_pending=True,
        backref=orm.backref('mac_learning', uselist=False,
                            cascade='delete', lazy='joined'))

    revises_on_change = ('port',)
