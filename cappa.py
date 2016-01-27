from __future__ import print_function

import os
import sys
import cytoolz
import operator
import subprocess
import platform
import json
import collections
import six
from distutils.spawn import find_executable
from contextlib import contextmanager


__all__ = ('CapPA',)


class MissingExecutable(Exception):
    """Exception raised when a package manager executable is missing"""
    pass


class UnknownManager(Exception):
    """Exception raised when a requested package manager is unknown"""
    pass


def warn(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

IS_MAC = 'Darwin' in platform.platform(terse=1)
IS_UBUNTU = platform.dist()[0] == 'Ubuntu'


class CapPA(object):
    ALL_MANAGERS = ('npm', 'npmg', 'bower', 'tsd', 'pip', 'pip3', 'pip_pypy', 'sys', 'Captricity')

    def __init__(self, warn_mode, private_https_oauth=False, use_venv=True):
        self.npm = find_executable('npm')
        self.bower = find_executable('bower')
        self.tsd = find_executable('tsd')
        self.pip = find_executable('pip')
        self.pip3 = find_executable('pip3')
        self.pip_pypy = find_executable('pip')
        # TODO: support for osx
        self.sys = find_executable('apt-get')
        self.warn_mode = warn_mode
        self.private_https_oauth = private_https_oauth
        self.use_venv = use_venv

    def install(self, packages, ignore_managers=None):
        if ignore_managers:
            packages = self._filter_packages(packages, ignore_managers)

        if isinstance(packages, dict):
            self._install_package_dict(packages)
        else:
            self._install_package_list(packages)

    def _assert_manager_exists(self, manager_type):
        manager_obj = getattr(self, manager_type)
        if manager_obj is None:
            manager_obj = find_executable(manager_type)  # Might have been installed in a previous step

        if manager_obj is None:
            if manager_type == 'pip_pypy':
                raise MissingExecutable('pip not found')
            elif manager_type == 'sys':
                raise MissingExecutable('apt-get not found')
            else:
                raise MissingExecutable('{} not found'.format(manager_type))
        else:
            if manager_type == 'pip_pypy':
                pypy_object = find_executable('pypy')
                if pypy_object is None:
                    raise MissingExecutable('pypy not found')
                return 'pip'
            return manager_obj

    def _install_package_dict(self, package_dict):
        if 'sys' in package_dict:
            self._update_apt_cache()

        for key, packages in six.iteritems(package_dict):
            try:
                if key == 'Captricity':
                    self._private_package_dict(packages)
                    self._install_package_dict(packages)
                    continue
                elif (key == 'npm' and
                      'name' in packages and
                      'version' in packages):
                    # Package list is actually a package.json file, so treat it as such
                    self._npm_package_json_install(packages)
                    continue
                elif key == 'bower':
                    self._setup_bower()
                    if ('name' in packages and 'version' in packages):
                        # Package list is actually a bower.json file, so treat it as such
                        self._bower_json_install(packages)
                        continue
                elif key == 'tsd':
                    if 'repo' in packages and 'path' in packages:
                        # Package list is actually a tsd.json file, so treat it as such
                        self._tsd_json_install(packages)
                        continue

                prefix = []
                options = []
                if key == 'npmg':
                    options.append('-g')
                    if not IS_MAC:
                        prefix.append('sudo')
                        prefix.append('-E')
                    key = 'npm'
                elif key == 'sys':
                    options.append('-y')
                    prefix.append('sudo')
                    prefix.append('-E')
                elif key in ['pip', 'pip3', 'pip_pypy'] and not self.use_venv:
                    prefix.append('sudo')
                    prefix.append('-E')
                if key == 'pip_pypy':
                    prefix.append('pypy')
                    prefix.append('-m')
                if key in ['pip', 'pip3', 'pip_pypy']:
                    subdir_packages, nonsubdir_packages = self._split_pip_packages(packages)
                    self._install_packages(key, subdir_packages, prefix, options + ['-e'])
                    self._install_packages(key, nonsubdir_packages, prefix, options)
                else:
                    self._install_packages(key, packages, prefix, options)
            except (UnknownManager, MissingExecutable) as e:
                if self.warn_mode:
                    warn(e)
                else:
                    raise e
            finally:
                self._clean_npm_residuals()
                self._clean_pip_residuals()

    def _install_package_list(self, packages):
        split = map(CapPA.extract_manager, packages)
        grouped_packages = cytoolz.itertoolz.groupby(operator.itemgetter(0), split)
        for key, packages in six.iteritems(grouped_packages):
            manager = self._assert_manager_exists(key)
            options = list(set(sum(map(operator.itemgetter(2), packages), [])))
            packages = map(operator.itemgetter(1), packages)
            if key == 'sys':
                prefix = ['sudo', '-E']
            else:
                prefix = []
            subprocess.check_call(prefix + [manager] + options + ['install'] + packages)

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

    def _private_package_dict(self, package_dict):
        # reconstruct package_dict based on private repo handling mode
        def repo_url(repo_string):
            repo_split = repo_string.split('@')
            if len(repo_split) > 1:
                repo, version = repo_split
            else:
                repo = repo_split[0]
                version = 'master'
            if self.private_https_oauth:
                # Use https with oauth. Pulls token from env
                token = os.environ['GITHUB_TOKEN']
                return 'git+https://{}@github.com/Captricity/{}.git@{}'.format(token, repo, version)
            else:
                return 'git+ssh://git@github.com/Captricity/{}.git@{}'.format(repo, version)

        for key in package_dict:
            package_dict[key] = {repo_url(repo): None for repo in package_dict[key]}

    def _npm_package_json_install(self, package_dict):
        npm = self._assert_manager_exists('npm')
        with self._chdir_to_target_if_set(package_dict):
            with open('package.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([npm, 'install'])
            os.remove('package.json')

    def _bower_json_install(self, package_dict):
        bower = self._assert_manager_exists('bower')
        with self._chdir_to_target_if_set(package_dict):
            with open('bower.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([bower, 'install'])
            os.remove('bower.json')

    def _setup_bower(self):
        bower_config = os.path.expanduser('~/.bowerrc')
        if not os.path.exists(bower_config):
            with open(bower_config, 'w') as f:
                f.write('{"analytics": false}')

    def _tsd_json_install(self, package_dict):
        tsd = self._assert_manager_exists('tsd')
        with self._chdir_to_target_if_set(package_dict):
            with open('tsd.json', 'w') as f:
                f.write(json.dumps(package_dict))
            subprocess.check_call([tsd, 'reinstall'])
            os.remove('tsd.json')

    def _clean_npm_residuals(self):
        """ Check for residual tmp files left by npm """
        if self.npm:
            tmp_location = subprocess.check_output(['npm', 'config', 'get', 'tmp'])
            tmp_location = tmp_location.strip()
            prefix = []
            if not IS_MAC:
                prefix.append('sudo')
                prefix.append('-E')
            subprocess.check_call(prefix + ['rm', '-rf', os.path.join(str(tmp_location), 'npm-*')])

    def _clean_pip_residuals(self):
        """ Check for residual tmp files left by pip """
        if self.pip or self.pip3 or self.pip_pypy:
            tmp_location = os.environ.get('TMPDIR',
                                          os.environ.get('TEMP',
                                                         os.environ.get('TMP', '/tmp')))
            tmp_location = tmp_location.strip()
            prefix = []
            if not IS_MAC:
                prefix.append('sudo')
                prefix.append('-E')
            subprocess.check_call(prefix + ['rm', '-rf', os.path.join(tmp_location, 'pip-*')])

    @contextmanager
    def _chdir_to_target_if_set(self, package_dict):
        cur_dir = os.getcwd()
        try:
            if 'target_dir' in package_dict:
                os.chdir(package_dict['target_dir'])
            yield
        finally:
            os.chdir(cur_dir)

    @staticmethod
    def extract_manager(package):
        if not (package.startswith('pip_pypy') or
                package.startswith('pip3') or
                package.startswith('pip') or
                package.startswith('bower') or
                package.startswith('npm')):
            raise UnknownManager("Could not identify base package manager for '{}'".format(package))

        split = package.split('-')
        package = '-'.join(split[1:])
        if split[0] == 'npmg':
            return 'npm', package, ['-g']
        return split[0], package, []

    def _filter_packages(self, packages, ignore_managers):
        if isinstance(packages, dict):
            new_packages = collections.OrderedDict()
            for k in packages:
                if k not in ignore_managers:
                    new_packages[k] = packages[k]
            return new_packages
        else:
            new_packages = []
            for package in packages:
                add_to_list = True
                for manager in ignore_managers:
                    if package.startswith(manager):
                        add_to_list = False
                if add_to_list:
                    new_packages.append(package)
            return new_packages

    def _install_packages(self, manager, packages, prefix, options):
        if not packages:
            return

        range_connector_gte = ">="
        range_connector_lt = "<"
        if manager == 'npm':
            connector = '@'
        elif manager == 'bower':
            connector = '#'
        elif manager in ['pip', 'pip3', 'pip_pypy']:
            connector = '=='
        elif manager == 'sys':
            connector = None  # does not support versioning
        else:
            raise UnknownManager("Could not identify base package manager '{}'".format(key))

        manager = self._assert_manager_exists(manager)
        args = prefix + [manager, 'install'] + options
        for package, version in six.iteritems(packages):
            if version is None or connector is None:
                args.append(package)
            elif isinstance(version, list):
                args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
            else:
                args.append(package + connector + version)
        subprocess.check_call(args, env=os.environ)

    def _split_pip_packages(self, packages):
        subdir_packages = {}
        nonsubdir_packages = {}
        for package, version in six.iteritems(packages):
            if 'subdirectory=' in package:
                subdir_packages[package] = version
            else:
                nonsubdir_packages[package] = version
        return subdir_packages, nonsubdir_packages
