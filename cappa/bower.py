

import os
import six
import json
import subprocess

from .base import CapPA


class Bower(CapPA):

    def __init__(self, *flags):
        super(Bower, self).__init__(*flags)
        self.name = 'bower'
        self.friendly_name = 'bower'

    def find_executable(self):
        local_bower = 'node_modules/.bin/bower'
        if os.path.exists(local_bower):
            return local_bower
        return super(Bower, self).find_executable()

    def _install_package_dict(self, packages):
        self._setup_bower()
        if 'name' in packages and 'version' in packages:
            # Package list is actually a package.json file, so treat it as such
            self._bower_json_install(packages)
            return

        range_connector_gte = ">="
        range_connector_lt = "<"
        connector = '#'
        manager = self.find_executable()
        args = [manager, 'install']
        for package, version in six.iteritems(packages):
            if version is None:
                args.append(package)
            elif isinstance(version, list):
                args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
            else:
                args.append(package + connector + version)
        subprocess.check_call(args, env=os.environ)

    def _setup_bower(self):
        bower_config = os.path.expanduser('~/.bowerrc')
        if not os.path.exists(bower_config):
            with open(bower_config, 'w') as f:
                f.write('{"analytics": false}')

    def _bower_json_install(self, package_dict):
        with self._chdir_to_target_if_set(package_dict):
            bower = self.find_executable()
            with open('bower.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([bower, 'install', '-f'])
            if not self.save_js:
                os.remove('bower.json')
