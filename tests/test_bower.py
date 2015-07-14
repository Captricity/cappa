from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES, BOWER_DEPENDENCIES


class CaptricityTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(NPM_DEPENDENCIES)
        self.install_requirements_json(BOWER_DEPENDENCIES)
        self.install_requirements_json(TEST_INSTALL_BOWER_VERSION_JSON)
        self.run_spec('bower_install_basic_spec')

TEST_INSTALL_BOWER_VERSION_JSON = """{
    "bower": {
        "name": "captricity",
        "version": "0.1.1",
        "description": "Captricity, Inc.",
        "dependencies": {
            "jquery": "2.1.4"
        },
        "private": true,
        "ignore": [
            "**/.*",
            "node_modules",
            "bower_components",
            "test",
            "tests"
        ]
    }
}"""

