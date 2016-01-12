from __future__ import absolute_import

from .base import VagrantTestCase
from fabric.api import task, sudo, cd

@task
def setup_python3_cappa():
    """Installs cappa on the vagrant box."""
    with cd('/vagrant'):
        sudo('apt-get -yy install python3-setuptools python3-dev')
        sudo('python3 setup.py install')


class Python3TestCases(VagrantTestCase):

    def _setup_cappa(self):
        self.run_fabric_task(setup_python3_cappa)

    def test_pip3(self):
        self.install_requirements_json(TEST_INSTALL_PIP3_VERSION_JSON)
        self.run_spec('pip3_install_basic_spec')


TEST_INSTALL_PIP3_VERSION_JSON = """{
    "sys": {
        "python3-pip": null,
        "git": null
    },
    "pip3": {
        "django": "1.8.5"
    }
}"""
