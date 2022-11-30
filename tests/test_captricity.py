from __future__ import absolute_import
from io import StringIO
from fabric.api import task, put, run, cd

from fabric.context_managers import settings

from .base import VagrantTestCase
from tests.dependencies import VIRTUALENV_DEPENDENCIES, PYTHON_DEPENDENCIES


class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(PYTHON_DEPENDENCIES)
        self.install_requirements_file(VIRTUALENV_DEPENDENCIES)
        self.run_fabric_task(self.install_requirements_json_captricity_factory(TEST_INSTALL_CAPTRICITY_VERSION_JSON))
        self.run_spec('captricity_install_basic_spec')

    def install_requirements_json_captricity_factory(self, requirements_json):

        @task
        def install_requirements_json_captricity():
            with cd('/home/vagrant'):
                put(StringIO(requirements_json), '/home/vagrant/requirements.json')
                run('virtualenv venv')
                run('echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> /home/vagrant/.ssh/config')
                with settings(forward_agent=True):
                    run('source venv/bin/activate; cappa install -r /home/vagrant/requirements.json')
        return install_requirements_json_captricity


TEST_INSTALL_CAPTRICITY_VERSION_JSON = """{
    "Captricity": {
        "pip": ["internal-api-clients@v0.0.3"]
    }
}"""
