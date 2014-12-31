import cytoolz
import operator
import subprocess
from distutils.spawn import find_executable

class MissingExecutable(Exception):
    pass
class UnknownManager(Exception):
    pass

class CapPA(object):
    def __init__(self):
        self.npm = find_executable('npm')
        self.bower = find_executable('bower')
        self.pip = find_executable('pip')

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

    def _install_package_dict(self, package_dict):
        for key, packages in package_dict.iteritems():
            if key == 'npmg':
                options = ['-g']
                key = 'npm'
            else:
                options = []

            if key == 'npm':
                connector = '@'
            elif key == 'bower':
                connector = '#'
            elif key == 'pip':
                connector = '=='
            else:
                raise UnknownManager('Could not identify base package manager \'{}\''.format(key))

            manager = getattr(self, key)
            self._assert_manager_exists(key, manager)
            args = [manager, 'install'] + options
            for package, version in packages.iteritems():
                if version is None:
                    args.append(package)
                else:
                    args.append(package + connector + version)
            subprocess.check_call(args)

    def _install_package_list(self, packages):
        split = map(CapPA.extract_manager, packages)
        for key, packages in cytoolz.itertoolz.groupby(operator.itemgetter(0), split).iteritems():
            manager = getattr(self, key)
            self._assert_manager_exists(key, manager)
            options = list(set(sum(map(operator.itemgetter(2), packages), [])))
            packages = map(operator.itemgetter(1), packages)
            subprocess.check_call([manager] + options + ['install'] + packages)

    @staticmethod
    def extract_manager(package):
        if not (package.startswith('pip') or package.startswith('bower') or package.startswith('npm')):
            raise UnknownManager('Could not identify base package manager for \'{}\''.format(package))

        split = package.split('-')
        package = '-'.join(split[1:])
        if split[0] == 'npmg':
            return 'npm', package, ['-g']
        return split[0], package, []
