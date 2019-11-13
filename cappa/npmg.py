

import os
import six
import subprocess

from .npm import Npm
from .enums import IS_MAC


class NpmG(Npm):

    def _install_package_dict(self, packages):
        range_connector_gte = ">="
        range_connector_lt = "<"
        connector = '@'
        manager = self.find_executable()
        prefix = []
        if not IS_MAC:
            prefix.append('sudo')
            prefix.append('-E')
        args = prefix + [manager, 'install', '-g']
        for package, version in six.iteritems(packages):
            if version is None:
                args.append(package)
            elif isinstance(version, list):
                args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
            else:
                args.append(package + connector + version)
        subprocess.check_call(args, env=os.environ)
