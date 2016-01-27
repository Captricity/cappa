from __future__ import absolute_import

import os
from cStringIO import StringIO

from fabric.api import task, put, run, cd

from fabric.context_managers import settings

from .base import VagrantTestCase
from tests.dependencies import PYTHON_DEPENDENCIES

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']


class RegressionTestCases(VagrantTestCase):

    def test_env_var_regression(self):
        """
        Cappa v0.9 had a bug where environment vars did not propagate to the
        sudo env when using the --no-venv option
        """
        self.install_requirements_json(PYTHON_DEPENDENCIES)
        self.run_fabric_task(self.install_requirements_json_captricity_factory(TEST_INSTALL_CAPTRICITY_VERSION_JSON))
        import pdb; pdb.set_trace()
        self.run_spec('env_var_regression')

    def install_requirements_json_captricity_factory(self, requirements_json):

        @task
        def install_requirements_json_captricity():
            with cd('/home/vagrant'):
                put(StringIO(requirements_json), '/home/vagrant/requirements.json')
                run('echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> /home/vagrant/.ssh/config')
                with settings(forward_agent=True):
                    run('GITHUB_TOKEN={} PIP_TARGET=/home/vagrant cappa install --private-https-oauth --no-venv -r /home/vagrant/requirements.json'.format(GITHUB_TOKEN))
        return install_requirements_json_captricity


TEST_INSTALL_CAPTRICITY_VERSION_JSON = """{
    "Captricity": {
        "pip": ["internal-api-clients@v0.0.3"]
    }
}"""
