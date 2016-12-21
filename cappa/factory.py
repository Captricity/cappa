from __future__ import print_function, absolute_import

from .ansible.apt import requirements_to_playbook_tasks as apt
from .ansible.pip import requirements_to_playbook_tasks as pip
from .ansible.npm import requirements_to_playbook_tasks as npm
from .ansible.npmg import requirements_to_playbook_tasks as npmg
from .ansible.bower import requirements_to_playbook_tasks as bower
from .exceptions import UnknownManager

"""
TODO:
    - pip3
    - pip_pypy
    - tsd
    - typings
    - yarn
    - yarng
    - private pip
    - private pip3
    - private apt
"""


MANAGER_MAP = {
    'sys': apt,
    'pip': pip,
    'npm': npm,
    'npmg': npmg,
    'bower': bower
}
PRIVATE_MANAGER_MAP = {
}


def manager_key_to_cappa(manager_key):
    if manager_key in MANAGER_MAP:
        return MANAGER_MAP[manager_key]
    else:
        raise UnknownManager('{} is not a supported manager.'.format(manager_key))


def private_manager_key_to_cappa(manager_key):
    if manager_key in PRIVATE_MANAGER_MAP:
        return PRIVATE_MANAGER_MAP[manager_key]
    else:
        raise UnknownManager('{} is not a supported private repo manager.'.format(manager_key))
