from __future__ import print_function, absolute_import

import os
import subprocess

from .base import CapPA
from .exceptions import UnknownManager
from .utils import warn
from .enums import IS_UBUNTU


class Apt(CapPA):

    def __init__(self, *flags):
        super(Apt, self).__init__(*flags)
        self.name = 'apt-get'
        self.friendly_name = 'apt-get'

    def _install_package_dict(self, packages):
        self._update_apt_cache()

        manager = self.find_executable()
        # Currently no versioning support for apt
        args = ['sudo', '-E', manager, 'install', '-y'] + list(packages.keys())
        subprocess.check_call(args, env=os.environ)

    def _update_apt_cache(self):
        # For now, only ubuntu is supported
        if not IS_UBUNTU:
            message = 'System packages only supported on Ubuntu'
            if self.warn_mode:
                warn(message)
                return
            else:
                raise UnknownManager(message)

        subprocess.check_call(['sudo', '-E', 'apt-get', 'update'])
