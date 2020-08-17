from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.collections import is_sequence


def postfix_type_join(mylist):
    if not is_sequence(mylist):
        raise AnsibleFilterError("list required, got %s" % type(mylist))

    ret_list = []

    for item in mylist:
        s = "%s:%s" % (item['type'], item['dest'])
        ret_list.append(s)

    return ", ".join(ret_list)


class FilterModule(object):
    def filters(self):
        return {
            'postfix_type_join': postfix_type_join
        }
