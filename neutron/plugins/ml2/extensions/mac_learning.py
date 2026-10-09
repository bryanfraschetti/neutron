from neutron_lib.plugins.ml2 import api
from oslo_log import log as logging

from neutron.db.models import mac_learning as mac_learning_model
from neutron.extensions import mac_learning


LOG = logging.getLogger(__name__)


class MacLearningExtensionDriver(api.ExtensionDriver):

    def initialize(self):
        LOG.info('MacLearningExtensionDriver initialization complete')

    @property
    def extension_alias(self):
        return mac_learning.ALIAS

    def process_create_port(self, context, data, result):
        enabled = data.get(mac_learning.MAC_LEARNING_ENABLED, False)
        if enabled:
            context.session.add(mac_learning_model.PortMacLearning(
                port_id=result['id'], mac_learning_enabled=enabled))
        result[mac_learning.MAC_LEARNING_ENABLED] = enabled

    def process_update_port(self, context, data, result):
        if mac_learning.MAC_LEARNING_ENABLED not in data:
            return
        enabled = data[mac_learning.MAC_LEARNING_ENABLED]
        record = context.session.query(
            mac_learning_model.PortMacLearning).filter_by(
                port_id=result['id']).one_or_none()
        if record:
            record.mac_learning_enabled = enabled
        elif enabled:
            context.session.add(mac_learning_model.PortMacLearning(
                port_id=result['id'], mac_learning_enabled=enabled))
        result[mac_learning.MAC_LEARNING_ENABLED] = enabled

    def extend_port_dict(self, session, port_db, result):
        if hasattr(port_db, 'mac_learning'):
            record = port_db.mac_learning
        else:
            record = session.query(
                mac_learning_model.PortMacLearning).filter_by(
                    port_id=result['id']).one_or_none()
        result[mac_learning.MAC_LEARNING_ENABLED] = (
            record.mac_learning_enabled if record else False)
