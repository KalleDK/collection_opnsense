from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import \
    check_purge_configured, builtin_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.purge import \
    purge, check_purge_filter
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule


# pylint: disable=R0915
def process(m: AnsibleModule, p: dict, r: dict) -> None:
    s = Session(module=m)
    meta_alias = Alias(module=m, session=s, result={})
    existing_aliases = meta_alias.get_existing()
    existing_rules = Rule(module=m, session=s, result={}).get_existing()
    aliases_to_purge = []

    def obj_func(alias_to_purge: dict) -> Alias:
        if p['debug'] or p['output_info']:
            m.warn(f"Purging alias '{alias_to_purge['name']}'!")

        if 'debug' not in aliases_to_purge:
            alias_to_purge['debug'] = p['debug']

        _alias = Alias(
            module=m,
            result={'changed': False, 'diff': {'before': {}, 'after': {}}},
            cnf=alias_to_purge,
            session=s,
            fail_verify=p['fail_all'],
            fail_proc=p['fail_all'],
        )
        _alias.alias = alias_to_purge
        _alias.existing_rules = existing_rules
        _alias.call_cnf['params'] = [alias_to_purge['uuid']]
        return _alias

    # checking if all aliases should be purged
    if not p['force_all'] and is_unset(p['aliases']) and \
            is_unset(p['filters']):
        m.fail_json("You need to either provide 'aliases' or 'filters'!")

    if p['force_all'] and is_unset(p['aliases']) and \
            is_unset(p['filters']):
        m.warn('Forced to purge ALL ALIASES!')

        for alias in existing_aliases:
            if not builtin_alias(name=alias['name']):
                purge(
                    module=m,
                    result=r,
                    diff_param='name',
                    obj_func=obj_func,
                    item_to_purge=alias,
                )

    else:
        # checking if existing alias should be purged
        for alias in existing_aliases:
            if not builtin_alias(name=alias['name']):
                to_purge = check_purge_configured(module=m, existing_alias=alias)

                if to_purge:
                    to_purge = check_purge_filter(module=m, item=alias)

                if to_purge:
                    if p['debug']:
                        m.warn(
                            f"Existing alias '{alias[p['key_field']]}' "
                            f"will be purged!"
                        )

                    aliases_to_purge.append(alias)

        for alias in aliases_to_purge:
            r['changed'] = True
            purge(
                module=m,
                result=r,
                diff_param='name',
                obj_func=obj_func,
                item_to_purge=alias,
            )

    if r['changed'] and p['reload']:
        meta_alias.reload()

    s.close()
