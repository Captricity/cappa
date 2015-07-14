from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import PYTHON_DEPENDENCIES, VIRTUALENV_DEPENDENCIES


class PipTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(PYTHON_DEPENDENCIES)
        self.install_requirements_json(VIRTUALENV_DEPENDENCIES)
        self.install_requirements_json_with_virtualenv(TEST_INSTALL_PIP_VERSION_JSON)
        self.run_spec('pip_install_basic_spec')


TEST_INSTALL_PIP_VERSION_JSON = """{
    "pip": {
        "django-extensions": "1.5.5"
    }
}"""
