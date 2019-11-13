

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES, TYPINGS_DEPENDENCIES


class TypingsTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(NPM_DEPENDENCIES)
        self.install_requirements_file(TYPINGS_DEPENDENCIES)
        self.install_requirements_file(TEST_TYPINGS_VERSION_JSON)
        self.run_spec('typings_install_basic_spec')


TEST_TYPINGS_VERSION_JSON = """{
    "typings": {
        "path": "typings",
        "dependencies": {
            "listify": "registry:npm/listify#1.0.0+20160211003958"
        }
    }
}"""
