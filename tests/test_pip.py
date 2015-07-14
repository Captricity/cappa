from __future__ import absolute_import

from .base import VagrantTestCase
from tests import assets

class PipTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(assets.TEST_NECESSARY_PIP_VIRTUALENV)
        self.install_requirements_json_virtualenv(TEST_INSTALL_PIP_VERSION_JSON)
        self.run_spec('pip_install_basic_spec')


TEST_INSTALL_PIP_VERSION_JSON = """{
    "pip": {
        "django-extensions": "1.5.5"
    }
}"""
