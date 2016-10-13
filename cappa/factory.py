from __future__ import print_function, absolute_import

from .pip import Pip
from .pip3 import Pip3
from .pip_pypy import PipPypy
from .apt import Apt
from .bower import Bower
from .npm import Npm
from .npmg import NpmG
from .yarn import Yarn
from .yarng import YarnG
from .tsd import Tsd
from .typings import Typings
from .exceptions import UnknownManager

from .private.pip import PrivatePip
from .private.pip3 import PrivatePip3


MANAGER_MAP = {
    'pip': Pip,
    'pip3': Pip3,
    'pip_pypy': PipPypy,
    'sys': Apt,
    'npm': Npm,
    'npmg': NpmG,
    'yarn': Yarn,
    'yarng': YarnG,
    'bower': Bower,
    'typings': Typings,
    'tsd': Tsd
}
PRIVATE_MANAGER_MAP = {
    'pip': PrivatePip,
    'pip3': PrivatePip3
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
