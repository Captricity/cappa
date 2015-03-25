from __future__ import print_function

import os
import sys
import cytoolz
import operator
import subprocess
import platform
import json
from distutils.spawn import find_executable
from contextlib import contextmanager

class MissingExecutable(Exception):
    pass
class UnknownManager(Exception):
    pass

def warn(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

class CapPA(object):
    def __init__(self, warn_mode, private_https_oauth=False):
        self.npm = find_executable('npm')
        self.bower = find_executable('bower')
        self.pip = find_executable('pip')
        # TODO: support for osx
        self.sys = find_executable('apt-get')
        self.warn_mode = warn_mode
        self.private_https_oauth = private_https_oauth

    def install(self, packages):
        if isinstance(packages, dict):
            self._install_package_dict(packages)
        else:
            self._install_package_list(packages)

    def _assert_manager_exists(self, manager_type, manager_obj):
        if manager_obj is None:
            if manager_type == 'npm':
                raise MissingExecutable('npm not found')
            if manager_type == 'bower':
                raise MissingExecutable('bower not found')
            if manager_type == 'pip':
                raise MissingExecutable('pip not found')
            if manager_type == 'sys':
                raise MissingExecutable('apt-get not found')

    def _install_package_dict(self, package_dict):
        if 'sys' in package_dict:
            self._update_apt_cache()

        for key, packages in package_dict.iteritems():
            try:
                prefix = []
                options = []
                if key == 'Captricity':
                    self._private_package_dict(packages)
                    self._install_package_dict(packages)
                    continue
                elif (key == 'npm' and
                      packages.has_key('name') and
                      packages.has_key('version')):
                    # Package list is actually a package.json file, so treat it as such
                    self._npm_package_json_install(packages)
                    continue
                elif (key == 'bower' and
                      packages.has_key('name') and
                      packages.has_key('version')):
                    # Package list is actually a bower.json file, so treat it as such
                    self._bower_json_install(packages)
                    continue
                elif key == 'npmg':
                    options.append('-g')
                    key = 'npm'
                elif key == 'sys':
                    options.append('-y')
                    prefix.append('sudo')
                elif key == 'pip':
                    options.append('-U')

                range_connector_gte = ">="
                range_connector_lt = "<"
                if key == 'npm':
                    connector = '@'
                elif key == 'bower':
                    connector = '#'
                elif key == 'pip':
                    connector = '=='
                elif key == 'sys':
                    connector = None # does not support versioning
                else:
                    raise UnknownManager('Could not identify base package manager \'{}\''.format(key))

                manager = getattr(self, key)
                self._assert_manager_exists(key, manager)
                args = prefix + [manager, 'install'] + options
                for package, version in packages.iteritems():
                    if version is None or connector is None:
                        args.append(package)
                    elif isinstance(version, list):
                        args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
                    else:
                        args.append(package + connector + version)
                subprocess.check_call(args)
            except (UnknownManager, MissingExecutable) as e:
                if self.warn_mode:
                    warn(e)
                else:
                    raise e

    def _install_package_list(self, packages):
        split = map(CapPA.extract_manager, packages)
        for key, packages in cytoolz.itertoolz.groupby(operator.itemgetter(0), split).iteritems():
            manager = getattr(self, key)
            self._assert_manager_exists(key, manager)
            options = list(set(sum(map(operator.itemgetter(2), packages), [])))
            packages = map(operator.itemgetter(1), packages)
            if key == 'sys':
                prefix = ['sudo']
            else:
                prefix = []
            subprocess.check_call(prefix + [manager] + options + ['install'] + packages)

    def _update_apt_cache(self):
        # For now, only ubuntu is supported
        if platform.dist()[0] != 'Ubuntu':
            message = 'System packages only supported on Ubuntu'
            if self.warn_mode:
                warn(message)
                return
            else:
                raise UnknownManager(message)

        subprocess.check_call(['sudo', 'apt-get', 'update'])

    def _private_package_dict(self, package_dict):
        # reconstruct package_dict based on private repo handling mode
        def repo_url(repo):
            if self.private_https_oauth:
                # Use https with oauth. Pulls token from env
                token = os.environ['GITHUB_TOKEN']
                return 'git+https://{}@github.com/Captricity/{}.git@master'.format(token, repo)
            else:
                return 'git+ssh://git@github.com/Captricity/{}.git@master'.format(repo)
        for key in package_dict:
            package_dict[key] = {repo_url(repo): None for repo in package_dict[key]}

    def _npm_package_json_install(self, package_dict):
        self._assert_manager_exists('npm', self.npm)
        with self._chdir_to_target_if_set(package_dict):
            with open('package.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([self.npm, 'install'])
            os.remove('package.json')

    def _bower_json_install(self, package_dict):
        self._assert_manager_exists('bower', self.bower)
        with self._chdir_to_target_if_set(package_dict):
            with open('bower.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([self.bower, 'install'])
            os.remove('bower.json')

    @contextmanager
    def _chdir_to_target_if_set(self, package_dict):
        cur_dir = os.getcwd()
        try:
            if package_dict.has_key('target_dir'):
                os.chdir(package_dict['target_dir'])
            yield
        finally:
            os.chdir(cur_dir)

    @staticmethod
    def extract_manager(package):
        if not (package.startswith('pip') or package.startswith('bower') or
                package.startswith('npm')):
            raise UnknownManager('Could not identify base package manager for \'{}\''.format(package))

        split = package.split('-')
        package = '-'.join(split[1:])
        if split[0] == 'npmg':
            return 'npm', package, ['-g']
        return split[0], package, []
