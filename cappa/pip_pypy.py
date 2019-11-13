

import os
import six
import subprocess
from distutils.spawn import find_executable

from .exceptions import MissingExecutable
from .pip import Pip


class PipPypy(Pip):

    def _install_package_dict(self, packages):
        def install(prefix, options, packages):
            range_connector_gte = ">="
            range_connector_lt = "<"
            connector = '=='
            args = prefix + ['pip', 'install'] + options
            for package, version in six.iteritems(packages):
                if version is None:
                    args.append(package)
                elif isinstance(version, list):
                    args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
                else:
                    args.append(package + connector + version)
            subprocess.check_call(args, env=os.environ)

        if not self.use_venv:
            prefix = ['sudo', '-E']
        prefix.append(self._find_pypy())
        prefix.append('-m')
        subdir_packages, nonsubdir_packages = self._split_pip_packages(packages)
        if subdir_packages:
            install(prefix, ['-e'], subdir_packages)
        if nonsubdir_packages:
            install(prefix, [], nonsubdir_packages)

    def _find_pypy(self):
        exe = find_executable('pypy')
        if exe is None:
            raise MissingExecutable('pypy not found')
        return exe
