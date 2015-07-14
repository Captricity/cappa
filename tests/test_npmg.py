from __future__ import absolute_import

from .base import VagrantTestCase
from tests import assets

class NpmgTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(assets.TEST_NECESSARY_PIP_VIRTUALENV)
        self.install_requirements_json_virtualenv(TEST_INSTALL_NPMG_VERSION_JSON)
        self.run_spec('npmg_install_basic_spec')


TEST_INSTALL_NPMG_VERSION_JSON = """{
    "sys": {
        "npm": null
    },
    "npmg": {
        "jshint": "2.8.0"
    }
}"""
