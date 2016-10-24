from __future__ import print_function, absolute_import

import os
import six
import subprocess

from .base import CapPA
from .enums import IS_MAC


class YarnG(CapPA):

    def __init__(self, *flags):
        super(YarnG, self).__init__(*flags)
        self.name = 'yarn'
        self.friendly_name = 'yarn'

    def _install_package_dict(self, packages):
        range_connector_gte = ">="
        range_connector_lt = "<"
        connector = '@'
        manager = self.find_executable()
        args = []
        if not IS_MAC:
            args.append('sudo')
            args.append('-E')
        args.extend([manager, 'global', 'add'])
        for package, version in six.iteritems(packages):
            if version is None:
                args.append(package)
            elif isinstance(version, list):
                args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
            else:
                args.append(package + connector + version)
        subprocess.check_call(args, env=os.environ)
