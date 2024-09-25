.. _modules_dhcrelay_relay:

.. include:: ../_include/head.rst

=============================
DHCRelay - Relay
=============================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/dhcrelay_destination.yml>`_

**API Docs**: `Core - DHCRelay <https://docs.opnsense.org/development/api/core/dhcrelay.html>`_

**Service Docs**: `DHCRelay <https://docs.opnsense.org/manual/dhcp.html#dhcrelay>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","false","\-","Enable or disable this relay"
    "interface","string","true","","i, int"," The interface to relay DHCP requests from"
    "destination","string","true","\-","dest"," The destination server group to relay DHCP requests to"
    "agent_info","boolean","false","false","\-","Add the relay agent information option"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DHCRelay relays. Each interface can be assigned a single relay.


Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dhcrelay_relay'

      tasks:
        - name: Example
          ansibleguy.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp
            # enabled: false
            # agent_info: false
            # state: 'present'
            # reload: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp

        - name: Removing
          ansibleguy.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp
            state: 'absent'

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'dhcrelay_relay'
          register: existing_entries

        - name: Printing dhcrelay relays
          ansible.builtin.debug:
            var: existing_entries.data
