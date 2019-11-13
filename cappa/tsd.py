

import os
import json
import subprocess

from .base import CapPA


class Tsd(CapPA):

    def __init__(self, *flags):
        super(Tsd, self).__init__(*flags)
        self.name = 'tsd'
        self.friendly_name = 'tsd'

    def _install_package_dict(self, packages):
        if 'repo' in packages and 'path' in packages:
            # Package list is actually a tsd.json file, so treat it as such
            self._tsd_json_install(packages)
        else:
            raise NotImplementedError()

    def _tsd_json_install(self, package_dict):
        tsd = self.find_executable()
        with self._chdir_to_target_if_set(package_dict):
            with open('tsd.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([tsd, 'reinstall'])
            if not self.save_js:
                os.remove('tsd.json')
