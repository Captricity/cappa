

import os
from distutils.spawn import find_executable
from contextlib import contextmanager

from .utils import warn
from .exceptions import MissingExecutable, UnknownManager


__all__ = ('CapPA',)


class CapPA(object):

    def __init__(self, warn_mode, private_https_oauth, use_venv, save_js):
        self.warn_mode = warn_mode
        self.private_https_oauth = private_https_oauth
        self.use_venv = use_venv
        self.save_js = save_js

    def install(self, packages):
        try:
            self._install_package_dict(packages)
        except (UnknownManager, MissingExecutable) as e:
            if self.warn_mode:
                warn(e)
            else:
                raise
        finally:
            self._clean()

    def find_executable(self):
        exe = find_executable(self.name)
        if exe is None:
            raise MissingExecutable('{} not found'.format(self.friendly_name))
        return exe

    def _clean(self):
        pass

    @contextmanager
    def _chdir_to_target_if_set(self, package_dict):
        cur_dir = os.getcwd()
        try:
            if 'target_dir' in package_dict:
                os.chdir(package_dict['target_dir'])
            yield
        finally:
            os.chdir(cur_dir)
