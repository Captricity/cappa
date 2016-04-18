from __future__ import print_function, absolute_import

from .pip import Pip
from .pip3 import Pip3
from .pip_pypy import PipPypy
from .apt import Apt
from .bower import Bower
from .npm import Npm
from .npmg import NpmG
from .tsd import Tsd

from .private.pip import PrivatePip


def manager_key_to_cappa(manager_key):
    if manager_key == 'pip':
        return Pip
    elif manager_key == 'pip3':
        return Pip3
    elif manager_key == 'pip_pypy':
        return PipPypy
    elif manager_key == 'sys':
        return Apt
    elif manager_key == 'npm':
        return Npm
    elif manager_key == 'npmg':
        return NpmG
    elif manager_key == 'bower':
        return Bower
    elif manager_key == 'tsd':
        return Tsd
    else:
        raise UnknownManager('{} is not a supported manager.'.format(manager_key))

def private_manager_key_to_cappa(manager_key):
    if manager_key == 'pip':
        return PrivatePip
    else:
        raise UnknownManager('{} is not a supported private repo manager.'.format(manager_key))
