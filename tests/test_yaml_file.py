from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import PYTHON_DEPENDENCIES, VIRTUALENV_DEPENDENCIES


class YamlTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(PYTHON_DEPENDENCIES)
        self.install_requirements_file(VIRTUALENV_DEPENDENCIES)
        self.install_requirements_file_with_virtualenv(TEST_INSTALL_PIP_VERSION_YAML)
        self.run_spec('pip_install_basic_spec')


TEST_INSTALL_PIP_VERSION_YAML = """
---
pip:
    django-extensions: 1.5.5
"""
