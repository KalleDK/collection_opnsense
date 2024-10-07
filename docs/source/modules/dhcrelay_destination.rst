.. _modules_dhcrelay_destination:

.. include:: ../_include/head.rst

=============================
DHCRelay - Destinations
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

    "name","string","true","","\-","Unique name for this relay destination"
    "server","list of strings","true","\-","\-","List of server IP addresses to relay DHCP requests to"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DHCRelay destinations. A destination can contain multiple IP addresses.

Note: You can also use the shortform module name: :code:`ansibleguy.opnsense.dhcrelay_dst`

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
          target: 'dhcrelay_destination'

      tasks:
        - name: Example
          ansibleguy.opnsense.dhcrelay_destination:
            name: 'mydhcp'
            server:
              - '192.168.0.1'
            # state: 'present'
            # reload: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.dhcrelay_destination:
            name: 'mydhcp'
            server:
              - '192.168.0.1'

        - name: Removing
          ansibleguy.opnsense.dhcrelay_destination:
            name: 'mydhcp'
            server:
              - '192.168.0.1'
            state: 'absent'

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'dhcrelay_destination'
          register: existing_entries

        - name: Printing dhcrelay destinations
          ansible.builtin.debug:
            var: existing_entries.data
