from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import YARN_DEPENDENCIES


class YarnTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(YARN_DEPENDENCIES)
        self.install_requirements_file(TEST_INSTALL_YARN_VERSION_JSON)
        self.run_spec('yarn_install_basic_spec')


TEST_INSTALL_YARN_VERSION_JSON = """{
    "yarn": {
        "underscore": "1.8.2"
    }
}"""
