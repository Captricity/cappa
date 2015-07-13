from __future__ import absolute_import
import os
from fabric.api import env, execute, task, sudo, put, run, cd

from .base import VagrantTestCase

class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        token = raw_input("Please enter your Github personal access tokens: ")
        self.run_fabric_task(self.setup_github_token_factory(token))
        self.install_requirements_json(TEST_INSTALL_CAPTRICITY_VERSION_JSON)
        # self.run_spec('captricity_install_basic_spec')
        print('Success!!!!!!!!!!!!!!!!!!!!!!!!')

    def setup_github_token_factory(self, token):
        @task
        def setup_github_token():
            with cd('/home/vagrant'):
                os.environ['GITHUB_TOKEN'] = token
                
        return setup_github_token

TEST_INSTALL_CAPTRICITY_VERSION_JSON = """{
    "Captricity": {
        "pip": ["internal-api-clients@v0.0.3"]
    }
}"""

#captsule@0.17 is repo + version
#pip and git

TEST_NECESSARY_PROVISIONERS = """{
    "sys": {
        "python-pip": null,
        "git": null
    }
}"""