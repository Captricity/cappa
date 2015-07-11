from __future__ import absolute_import

from .base import VagrantTestCase

class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        self.install_requirements_json(TEST_INSTALL_CAPTRICITY_VERSION_JSON)
        self.run_spec('captricity_install_basic_spec')


TEST_INSTALL_CAPTRICITY_VERSION_JSON = """{
    "Captricity": {
        "pip": null
    }
}"""


#pip and git

TEST_NECESSARY_PROVISIONERS = """{
    "sys": {
        "python-pip": null,
        "git": null
    }
}"""