from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES


class NpmgTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(NPM_DEPENDENCIES)
        self.install_requirements_json(TEST_INSTALL_NPMG_VERSION_JSON)
        self.run_spec('npmg_install_basic_spec')


TEST_INSTALL_NPMG_VERSION_JSON = """{
    "npmg": {
        "jshint": "2.8.0"
    }
}"""
