from __future__ import absolute_import
import os
from fabric.api import env, execute, task, sudo, put, run, cd
from fabric.context_managers import shell_env
from cStringIO import StringIO
from fabric.operations import local

from .base import VagrantTestCase

class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        token = 'bfab3cbff4afaec84cccbe1322ad3e2da525b2a1'
        # self.run_fabric_task(self.setup_github_token_factory(token))
        self.run_fabric_task(self.install_requirements_json_captricity_factory(TEST_INSTALL_CAPTRICITY_VERSION_JSON))
        self.run_spec('captricity_install_basic_spec')
        # print('Success!!!!!!!!!!!!!!!!!!!!!!!!')

    def install_requirements_json_captricity_factory(self, requirements_json):

        @task
        def install_requirements_json_captricity():
            # with shell_env(GITHUB_TOKEN=token):
            #     run('echo GITHUB_TOKEN is $GITHUB_TOKEN')
            with cd('/home/vagrant'):
                put(StringIO(requirements_json), '/home/vagrant/requirements.json')
                # os.putenv('GITHUB_TOKEN', token)
                run('cappa install --private-https-oauth --no-venv -r /home/vagrant/requirements.json')
        return install_requirements_json_captricity


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