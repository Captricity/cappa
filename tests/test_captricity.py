from __future__ import absolute_import
from .base import VagrantTestCase

from fabric.api import task, put, run, cd
from fabric.context_managers import settings
from cStringIO import StringIO


class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        self.install_requirements_json(TEST_NECESSARY_PIP_VIRTUALENV)
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

TEST_NECESSARY_PROVISIONERS = """{
    "sys": {
        "python-pip": null,
        "git": null
    }
}"""

TEST_NECESSARY_PIP_VIRTUALENV = """{
    "pip": {
        "virtualenv": null
    }
}"""