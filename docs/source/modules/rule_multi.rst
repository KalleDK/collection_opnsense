.. _modules_rule_multi:

.. include:: ../_include/head.rst

======================
Rule - Mass Management
======================

**STATE**: stable

**TESTS**: `rule_multi <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/rule_multi.yml>`_ |
`rule_purge <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/rule_multi.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Rules <https://docs.opnsense.org/manual/firewall.html#rules.html>`_

Info
****

For basic info, limitations and must-know to the rule-handling see the :ref:`ansibleguy.opnsense.rule <modules_rule>` module!

Multi
*****

- Each rule has the attributes as defined in the :ref:`'single' ansibleguy.opnsense.rule <modules_rule>` module

- To ensure valid configuration - the attributes of each rule get verified using ansible's built-in verifier

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.rule_multi
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "rules","dictionary","true","\-","\-","Dictionary of rules to manage/configure"
    "key_field","string","true","\-","\-","What field is used as key of the provided dictionary. One of: 'sequence', 'description', 'uuid'"
    "match_fields","list","true","\-","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'gateway', 'description', 'uuid'"
    "fail_verification","boolean","false","true","fail_verify","Fail module if single rule fails the verification"
    "fail_processing","boolean","false","true","fail_proc","Fail module if single rule fails to be processed"
    "override","dictionary","false","\-","\-","Parameters to override for all rules"
    "defaults","dictionary","false","\-","\-","Default values for all rules"
    "state","string","false","'present'","\-","Options: 'present', 'absent'"
    "enabled","boolean","false","true","\-","If all rules should be en- or disabled"
    "output_info","boolean","false","false","info","Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'."
    "reload","boolean","false","true","apply", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.rule_purge
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "rules","dictionary","true","\-","\-","Configured rules - to exclude from purging"
    "key_field","string","true","\-","\-","What field is used as key of the provided dictionary. One of: 'sequence', 'description', 'uuid'"
    "match_fields","list","true","\-","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'gateway', 'description', 'uuid'"
    "output_info","boolean","false","false","info","Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'."
    "action","string","false","'delete'","\-","What to do with the matched rules. One of: 'disable', 'delete'"
    "filters","dictionary","false","\-","\-","Field-value pairs to filter on - per example: {interface: lan} - to only purge rules that have only lan as interface"
    "filter_invert","boolean","false","false","\-","If true - it will purge all but the filtered ones"
    "filter_partial","boolean","false","false","\-","If true - the filter will also match if it is just a partial value-match"
    "force_all","boolean","false","false","\-","'If set to true and neither rules, nor filters are provided - all rules will be purged"
    "fail_all","boolean","false","false","fail","Fail module if single rule fails to be purged"

Usage
*****

The 'rule_multi' module is meant to manage dictionaries of rules.

You could either invoke this module:

- once for all rules
- once per logical grouping of rules


Examples
********

Basics
======

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.rule_multi:
          match_fields: ['description']
          key_field: 'description'  # rule-field that is used as key of the 'rules' dictionary

        ansibleguy.opnsense.list:
          target: 'rule'

        ansibleguy.opnsense.rule_purge:
          match_fields: ['description']
          key_field: 'description'

      tasks:
        - name: Changing
          ansibleguy.opnsense.rule_multi:
            rules:
              test1:
                source_net: '192.168.1.0/24'
                destination_invert: true
                destination_net: '10.1.0.0/8'
                action: 'block'
              test2:
                source_net: '192.168.0.0/16'
                destination_net: '10.156.10.0/24'
                destination_port: 8080
                protocol: 'TCP'
                interface: ['lan', 'opt1']
              test3:
                src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
                int: 'wan'
                action: 'block'
              test4:
                src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
                int: 'wan'
                action: 'block'
                ip_proto: 'inet6'
                state: 'absent'
            # match_fields: ['description']
            # key_field: 'description'
            # fail_verification: false
            # fail_processing: false
            # output_info: false
            # reload: true

        - name: Pulling existing rules
          ansibleguy.opnsense.list:
          #  target: 'rule'
          register: existing_entries

        - name: Printing rules
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Purging all non-configured rules
          ansibleguy.opnsense.rule_purge:
            rules: {...}
            # action: 'disable'  # default = remove
            # match_fields: ['description']
            # key_field: 'description'

        - name: Purging allow-rules on interface opt2 that use IPv4
          ansibleguy.opnsense.rule_purge:
            filters:  # filtering rules to purge by rule-parameters
              ip_protocol: 'inet'
              action: 'allow'
              interface: ['opt2']
            # filter_invert: true  # purge all non-port rules
            # match_fields: ['description']
            # key_field: 'description'

Options
=======

You can also override all rule parameters as needed.

.. code-block:: yaml

    - name: Changing
      ansibleguy.opnsense.rule_multi:
        rules: {...}

        # set parameters and/or states to all rules
        override:
          interface: ['lan', 'opt1', 'opt2']
          log: true

        state: 'absent'
        enabled: false

        # or set default values for all rules (override the built-in default values)
        defaults:
          action: 'block'
          sequence: 50

        # match_fields: ['description']
        # key_field: 'description'

To simplify the modules usage and config - you can also use shorter parameter aliases.

.. code-block:: yaml

    - name: Changing
      ansibleguy.opnsense.rule_multi:
        rules:
          test1:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
          test2:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
            ip_proto: 'inet6'
            state: 'absent'
          test3:
            s: '192.168.0.0/16'  # source
            d: '10.81.53.0/24'  # destination
            dp: 443  # destination_port
            p: 'TCP'  # protocol
            i: ['lan', 'opt1']  # interface
            en: false  # enabled

        # match_fields: ['description']
        # key_field: 'description'

Troubleshooting
===============

- info
- debug overall
- debug per rule

To simplify troubleshooting of bad configuration there are some troubleshooting parameters available.


.. code-block:: yaml

    - name: Changing
      ansibleguy.opnsense.rule_multi:
        rules: {...}
        fail_verification: true  # if the module should fail if one rule has a bad config (default behaviour)
        output_info: true  # to output information of processed rules
        debug: true  # output verbose information about requests and processing


Logical grouping
================

This example shows an option how to manage complexer rule-sets and/or template rules across multiple sites.

Basically we are abstracting the rule-set into interface-groups (*I'll call them zones*)

.. code-block:: yaml

    to be done
