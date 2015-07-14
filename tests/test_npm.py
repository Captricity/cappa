from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES


class NpmTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(NPM_DEPENDENCIES)
        self.install_requirements_json(TEST_INSTALL_NPM_VERSION_JSON)
        self.run_spec('npm_install_basic_spec')


TEST_INSTALL_NPM_VERSION_JSON = """{
    "npm": {
        "underscore": "1.8.2"
    }
}"""
