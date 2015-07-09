from __future__ import absolute_import

from .base import VagrantTestCase

class NpmgTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        self.install_requirements_json(TEST_INSTALL_NPMG_VERSION_JSON)
        self.run_spec('npmg_install_basic_spec')


TEST_INSTALL_NPMG_VERSION_JSON = """{
    "npmg": {
        "bower": "1.4.1"
        "gulp": "3.8.7"
    }
}"""


TEST_NECESSARY_PROVISIONERS = """{
    "sys": {
        "npm": null
    }
}"""