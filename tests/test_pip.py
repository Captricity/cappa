

from .base import VagrantTestCase
from fabric.api import task, sudo, run, cd
from tests.dependencies import PYTHON_DEPENDENCIES, VIRTUALENV_DEPENDENCIES


@task
def setup_pypy():
    """Installs pypy on the vagrant box."""
    sudo('add-apt-repository -y ppa:pypy/ppa')
    sudo('apt-get -y update')
    sudo('apt-get -y install pypy')
    with cd('~'):
        run('curl -O https://bootstrap.pypa.io/get-pip.py')
        sudo('pypy get-pip.py')


class PipTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(PYTHON_DEPENDENCIES)
        self.install_requirements_file(VIRTUALENV_DEPENDENCIES)
        self.install_requirements_file_with_virtualenv(TEST_INSTALL_PIP_VERSION_JSON)
        self.run_spec('pip_install_basic_spec')

    def test_pip3(self):
        self.install_requirements_file(TEST_INSTALL_PIP3_VERSION_JSON)
        self.run_spec('pip3_install_basic_spec')

    def test_pip_pypy(self):
        self.run_fabric_task(setup_pypy)
        self.install_requirements_file(TEST_INSTALL_PIPPYPY_VERSION_JSON)
        self.run_spec('pip_pypy_install_basic_spec')

TEST_INSTALL_PIP_VERSION_JSON = """{
    "pip": {
        "django-extensions": "1.5.5"
    }
}"""

TEST_INSTALL_PIP3_VERSION_JSON = """{
    "sys": {
        "python3-pip": null,
        "git": null
    },
    "pip3": {
        "django": "1.8.5"
    }
}"""

TEST_INSTALL_PIPPYPY_VERSION_JSON = """{
    "pip_pypy": {
        "django": "1.8.5"
    }
}"""
