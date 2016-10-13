from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import YARN_DEPENDENCIES


class NpmgTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(YARN_DEPENDENCIES)
        self.install_requirements_file(TEST_INSTALL_YARNG_VERSION_JSON)
        self.run_spec('yarng_install_basic_spec')


TEST_INSTALL_YARNG_VERSION_JSON = """{
    "yarng": {
        "jshint": "2.8.0"
    }
}"""
