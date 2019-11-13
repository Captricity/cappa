

import os
import six
import subprocess

from .base import CapPA
from .enums import IS_MAC
from .utils import warn


class Pip(CapPA):

    def __init__(self, *flags):
        super(Pip, self).__init__(*flags)
        self.name = 'pip'
        self.friendly_name = 'pip'

    def _install_package_dict(self, packages):
        def install(prefix, options, packages):
            range_connector_gte = ">="
            range_connector_lt = "<"
            connector = '=='
            manager = self.find_executable()
            args = prefix + [manager, 'install'] + options
            for package, version in six.iteritems(packages):
                if version is None:
                    args.append(package)
                elif isinstance(version, list):
                    args.append(package + range_connector_gte + version[0] + ',' + range_connector_lt + version[1])
                else:
                    args.append(package + connector + version)
            subprocess.check_call(args, env=os.environ)

        prefix = []
        if not self.use_venv:
            prefix.append('sudo')
            prefix.append('-E')
        subdir_packages, nonsubdir_packages = self._split_pip_packages(packages)
        if subdir_packages:
            install(prefix, ['-e'], subdir_packages)
        if nonsubdir_packages:
            install(prefix, [], nonsubdir_packages)

    def _clean(self):
        """ Check for residual tmp files left by pip """
        tmp_location = os.environ.get('TMPDIR',
                                      os.environ.get('TEMP',
                                                     os.environ.get('TMP', '/tmp')))
        tmp_location = tmp_location.strip()
        prefix = []
        if not IS_MAC:
            prefix.append('sudo')
            prefix.append('-E')
        try:
            subprocess.check_call(prefix + ['rm', '-rf', os.path.join(tmp_location, 'pip-*')])
        except Exception as exc:
            warn('error removing pip files', exc)

    def _split_pip_packages(self, packages):
        subdir_packages = {}
        nonsubdir_packages = {}
        for package, version in six.iteritems(packages):
            if 'subdirectory=' in package:
                subdir_packages[package] = version
            else:
                nonsubdir_packages[package] = version
        return subdir_packages, nonsubdir_packages
