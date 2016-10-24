from __future__ import absolute_import

from .test_yarn import setup_yarn
from .base import VagrantTestCase
from tests.dependencies import YARN_DEPENDENCIES


class YarngTestCases(VagrantTestCase):

    def test_basic(self):
        self.run_fabric_task(setup_yarn)
        self.install_requirements_file(YARN_DEPENDENCIES)
        self.install_requirements_file(TEST_INSTALL_YARNG_VERSION_JSON)
        self.run_spec('yarng_install_basic_spec')


TEST_INSTALL_YARNG_VERSION_JSON = """{
    "yarng": {
        "jshint": "2.8.0"
    }
}"""
