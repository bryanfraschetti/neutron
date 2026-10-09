from neutron_lib.api import converters
from neutron_lib.api import extensions


ALIAS = 'mac-learning'
MAC_LEARNING_ENABLED = 'mac_learning_enabled'

RESOURCE_ATTRIBUTE_MAP = {
    'ports': {
        MAC_LEARNING_ENABLED: {
            'allow_post': True,
            'allow_put': True,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True,
        },
    },
}


class Mac_learning(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return 'Port MAC Learning'

    @classmethod
    def get_alias(cls):
        return ALIAS

    @classmethod
    def get_description(cls):
        return 'Enable MAC learning for an OVN port with port security.'

    @classmethod
    def get_updated(cls):
        return '2026-10-09T00:00:00-00:00'

    def get_extended_resources(self, version):
        return RESOURCE_ATTRIBUTE_MAP if version == '2.0' else {}
