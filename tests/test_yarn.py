from __future__ import absolute_import

from fabric.api import task, sudo, run
from .base import VagrantTestCase
from tests.dependencies import YARN_DEPENDENCIES


@task
def setup_yarn():
    """Installs yarn on the vagrant box."""
    # Need later version of nodejs...
    sudo('curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -')

    # ...to get yarn
    sudo('apt-key adv --keyserver pgp.mit.edu --recv D101F7899D41F3C3')
    run('echo "deb http://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')


class YarnTestCases(VagrantTestCase):

    def test_basic(self):
        self.run_fabric_task(setup_yarn)
        self.install_requirements_file(YARN_DEPENDENCIES)
        self.install_requirements_file(TEST_INSTALL_YARN_VERSION_JSON)
        self.run_spec('yarn_install_basic_spec')


TEST_INSTALL_YARN_VERSION_JSON = """{
    "yarn": {
        "underscore": "1.8.2"
    }
}"""
