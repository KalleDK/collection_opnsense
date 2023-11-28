#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/bind.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.bind_record import \
        RECORD_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_record import \
        Record

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'


def run_module():
    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=RECORD_MOD_ARGS,
        supports_check_mode=True,
    )

    r = Record(module=module, result=result)

    def process():
        r.check()
        r.process()
        if result['changed'] and module.params['reload']:
            r.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='bind_record.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    r.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
