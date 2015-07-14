from __future__ import absolute_import

from .base import VagrantTestCase
from tests import assets

class NpmTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(assets.TEST_NECESSARY_PIP_VIRTUALENV)
        self.install_requirements_json_virtualenv(TEST_INSTALL_NPM_VERSION_JSON)
        self.run_spec('npm_install_basic_spec')


TEST_INSTALL_NPM_VERSION_JSON = """{
    "sys": {
        "npm": null
    },
    "npm": {
        "underscore": "1.8.2"
    }
}"""
