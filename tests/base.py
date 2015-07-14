import unittest
import vagrant
import subprocess
from cStringIO import StringIO
from fabric.api import env, execute, task, sudo, put, run, cd


@task
def setup_cappa():
    """Installs cappa on the vagrant box."""
    with cd('/vagrant'):
        sudo('python setup.py install')


def install_requirements_without_virtualenv(requirements_json):
    """Given the contents of the requirements.json file, this will return a
    fabric task that will create the file on the remote machine and install the
    requirements using cappa.
    """

    @task
    def requirements_json_install():
        with cd('/home/vagrant'):
            put(StringIO(requirements_json), '/home/vagrant/requirements.json')
            run('cappa install --no-venv -r /home/vagrant/requirements.json')

    return requirements_json_install

def install_requirements(requirements_json):
    """Given the contents of the requirements.json file, this will return a
    fabric task that will create the file on the remote machine and install the
    requirements using cappa.
    """

    @task
    def requirements_json_install_virtualenv():
        with cd('/home/vagrant'):
            put(StringIO(requirements_json), '/home/vagrant/requirements.json')
            run('virtualenv venv')
            run('source venv/bin/activate; cappa install -r /home/vagrant/requirements.json')

    return requirements_json_install_virtualenv


class VagrantTestCase(unittest.TestCase):
    """Baseclass for Vagrant test cases

    At the start of the test case, this will create a new vagrant box, and
    install cappa in it. Test cases can then interact with vagrant using
    `self.vagrant`, or execute tasks against it using `self.run_fabric_task`.
    The state of the vagrant machine can then be tested using serverspec and
    `self.run_spec`. The vagrant box is destroyed at the end of each test, to
    ensure a clean box for each test.
    """

    def setUp(self):
        self._setup_vagrant()
        self._setup_cappa()

    def tearDown(self):
        self.vagrant.destroy()

    def _setup_vagrant(self):
        """Ensure a vagrant machine exists."""
        self.vagrant = vagrant.Vagrant()
        box_status = self.vagrant.status()[0]
        if box_status.state == vagrant.Vagrant.RUNNING:
            self.vagrant.destroy()

        self.vagrant.up()

    def _setup_cappa(self):
        """Ensure cappa is installed."""
        self.run_fabric_task(setup_cappa)

    def install_requirements_json(self, requirements_json):
        """Given the contents of the requirements.json file, upload to vagrant
        box and install it.
        """
        self.run_fabric_task(install_requirements_without_virtualenv(requirements_json))

    def install_requirements_json_with_virtualenv(self, requirements_json):
        """Same as the funciton above, except run in virtual env."""
        self.run_fabric_task(install_requirements(requirements_json))

    def run_spec(self, spec_name):
        """Meat of the framework. Will run the specified serverspec file.

        The serverspec test must exist in `tests/serverspecs/spec/default`.
        """
        p = subprocess.Popen(['rake', 'spec', 'SPEC=spec/default/{}.rb'.format(spec_name)],
                             cwd='tests/serverspecs',
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print stdout
        print stderr
        if p.returncode:
            raise Exception(stdout)

    def run_fabric_task(self, fabric_task):
        """Execute a fabric task against the provisioned vagrant box."""
        env.hosts = [self.vagrant.user_hostname_port()]
        env.key_filename = self.vagrant.keyfile()
        env.disable_known_hosts
        execute(fabric_task)
