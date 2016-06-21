from __future__ import print_function, absolute_import

import os
import json
import subprocess

from .base import CapPA


class Typings(CapPA):

    def __init__(self, *flags):
        super(Typings, self).__init__(*flags)
        self.name = 'typings'
        self.friendly_name = 'typings'

    def _install_package_dict(self, packages):
        if 'dependencies' in packages and 'path' in packages:
            # Package list is actually a typings.json file, so treat it as such
            self._typings_json_install(packages)
        else:
            raise NotImplementedError()

    def _typings_json_install(self, package_dict):
        typings = self.find_executable()
        with self._chdir_to_target_if_set(package_dict):
            with open('typings.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([typings, 'install'])
            if not self.save_js:
                os.remove('typings.json')
