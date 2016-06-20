from __future__ import print_function, absolute_import

import os
import six
import json
import subprocess

from .base import CapPA
from .enums import IS_MAC


class Npm(CapPA):

    def __init__(self, *flags):
        super(Npm, self).__init__(*flags)
        self.name = 'npm'
        self.friendly_name = 'npm'

    def _install_package_dict(self, packages):
        if 'name' in packages and 'version' in packages:
            # Package list is actually a package.json file, so treat it as such
            self._npm_package_json_install(packages)
            return

        range_connector_gte = ">="
        range_connector_lt = "<"
        connector = '@'
        manager = self.find_executable()
        args = [manager, 'install', '--progress=false']
        for package, version in six.iteritems(packages):
            if version is None:
                args.append(package)
            elif isinstance(version, list):
                args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
            else:
                args.append(package + connector + version)
        subprocess.check_call(args, env=os.environ)

    def _clean(self):
        """ Check for residual tmp files left by npm """
        tmp_location = subprocess.check_output(['npm', 'config', 'get', 'tmp'])
        tmp_location = tmp_location.strip()
        prefix = []
        if not IS_MAC:
            prefix.append('sudo')
            prefix.append('-E')
        subprocess.check_call(prefix + ['rm', '-rf', os.path.join(str(tmp_location), 'npm-*')])

    def _npm_package_json_install(self, package_dict):
        npm = self.find_executable()
        with self._chdir_to_target_if_set(package_dict):
            with open('package.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([npm, 'install', '--progress=false'])
            if not self.save_js:
                os.remove('package.json')
