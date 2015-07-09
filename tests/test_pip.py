from __future__ import absolute_import

from .base import VagrantTestCase

class PipTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(TEST_NECESSARY_PROVISIONERS)
        self.install_requirements_json(TEST_INSTALL_PIP_VERSION_JSON)
        self.run_spec('pip_install_basic')


TEST_INSTALL_PIP_VERSION_JSON = """{
    "pip": {
        "django-extensions": "1.5.5"
    }
}"""

TEST_NECESSARY_PROVISIONERS = """{
    "sys": {
        "python-pip": null
    }
}"""