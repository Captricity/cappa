import unittest
import vagrant
import subprocess
from io import StringIO
import os
from fabric.api import env, execute, task, sudo, put, run, cd
from subprocess import call


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
        os.mkdir('/home/cappa')
        os.mkdir('/home/cappa/test')
        os.chdir('/home/cappa/test')
        put({StringIO(requirements_json)}, '/home/cappa/test/requirements.json')
        call('cappa install --no-venv -r /home/cappa/test/requirements.json', shell=True) 

    return requirements_json_install


def install_requirements(requirements_json, ext):
    """Given the contents of the requirements.json/yaml file, this will return a
    fabric task that will create the file on the remote machine and install the
    requirements using cappa.
    """

    @task
    def requirements_json_install_virtualenv():
        with cd('/home/vagrant'):
            fname = '/home/vagrant/requirements.' + ext
            put(StringIO(requirements_json), fname)
            run('virtualenv venv')
            run('source venv/bin/activate; cappa install -r ' + fname)

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
        #self._setup_vagrant()
        #self._setup_cappa()
        pass

    def tearDown(self):
        #self.vagrant.destroy()
        pass

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

    def install_requirements_file(self, requirements_file):
        """Given the contents of the requirements.json/yaml file, upload to vagrant
        box and install it.
        """
        self.run_fabric_task(install_requirements_without_virtualenv(requirements_file))

    def install_requirements_file_with_virtualenv(self, requirements_json, ext='json'):
        """Same as the funciton above, except run in virtual env."""
        self.run_fabric_task(install_requirements(requirements_json, ext))

    def run_spec(self, spec_name):
        """Meat of the framework. Will run the specified serverspec file.

        The serverspec test must exist in `tests/serverspecs/spec/default`.
        """
        p = subprocess.Popen(['rake', 'spec', 'SPEC=spec/default/{}.rb'.format(spec_name)],
                             cwd='tests/serverspecs',
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print(stdout)
        print(stderr)
        if p.returncode:
            raise Exception(stdout)

    def run_fabric_task(self, fabric_task):
        """Execute a fabric task against the provisioned vagrant box."""
        # env.hosts = [self.vagrant.user_hostname_port()]
        # env.key_filename = self.vagrant.keyfile()
        # env.disable_known_hosts
        execute(fabric_task)
