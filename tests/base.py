import unittest
import vagrant
from fabric.api import env, execute, task, sudo, cd

@task
def setup_cappa():
    with cd('/vagrant'):
        sudo('apt-get -qq update')
        sudo('apt-get -y install build-essential python-dev python-setuptools')
        sudo('python setup.py install')

class VagrantTestCase(unittest.TestCase):

    def setUp(self):
        self._setup_vagrant()
        self._setup_cappa()

    def tearDown(self):
        self.vagrant.destroy()

    def _setup_vagrant(self):
        self.vagrant = vagrant.Vagrant()
        box_status = self.vagrant.status()[0]
        if box_status.state == vagrant.Vagrant.RUNNING:
            self.vagrant.destroy()

        self.vagrant.up()

    def _setup_cappa(self):
        env.hosts = [self.vagrant.user_hostname_port()]
        env.key_filename = self.vagrant.keyfile()
        env.disable_known_hosts
        execute(setup_cappa)
