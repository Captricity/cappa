from __future__ import absolute_import

import subprocess
from fabric.api import env, execute, task, run, sudo, cd
from .base import VagrantTestCase

class SystemTestCases(VagrantTestCase):

    def test_basic(self):
        p = subprocess.Popen(['rake', 'spec'], cwd='tests/serverspecs/system_basic_spec', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print stdout
        print stderr
        if p.returncode:
            raise Exception(stdout)
