Per-port MAC learning
====================

The experimental ``mac-learning`` extension exposes a boolean port attribute,
``mac_learning_enabled``, which defaults to ``false``. Enable this extension
only with ML2/OVN and OVN builds supporting FDB learning on ports with non-empty
``port_security``. The OVN patch removing that learning exclusion is required;
Neutron does not automatically detect it. Unpatched OVN can lose connectivity
to allowed-address-pair MACs when this attribute is enabled.

Apply the database migration with ``neutron-db-manage upgrade heads`` and add
``mac_learning`` to the existing ``[ml2] extension_drivers`` list on every
Neutron server. Restart the servers after installing the updated package.

Create a port using the Networking API ``POST /v2.0/ports`` with, for example:

.. code-block:: json

   {
     "port": {
       "network_id": "NETWORK_UUID",
       "mac_learning_enabled": true,
       "allowed_address_pairs": [
         {"mac_address": "00:00:5e:00:01:01", "ip_address": "172.16.11.1"}
       ]
     }
   }

Enable learning on an existing port using ``PUT /v2.0/ports/PORT_UUID``:

.. code-block:: json

   {"port": {"mac_learning_enabled": true}}

Send ``false`` to restore static forwarding. The attribute is returned by port
create, update, show and list operations. Dedicated OpenStackClient options
require separate SDK/client changes and are not provided by this extension.

For normal logical switch ports with learning enabled, Neutron includes
``unknown`` and the port's own MAC/fixed IPs in ``addresses``, but does not
include additional allowed-address-pair MACs there. Their MAC/IP and VRRPv3
entries remain in ``port_security``. Enable this on each participating port
when a shared MAC must move between hosts; the newly active host must transmit
with that Ethernet source MAC to trigger learning. Only one host should use
the shared source MAC at a time.

Special logical switch port types retain their existing address behavior.
Ports with security disabled also retain their existing behavior. Setting the
attribute does not change security groups or the port-security allowlist.
