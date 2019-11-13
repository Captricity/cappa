

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES, TSD_DEPENDENCIES


class TsdTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_file(NPM_DEPENDENCIES)
        self.install_requirements_file(TSD_DEPENDENCIES)
        self.install_requirements_file(TEST_TSD_VERSION_JSON)
        self.run_spec('tsd_install_basic_spec')


TEST_TSD_VERSION_JSON = """{
    "tsd": {
        "version": "v4",
        "repo": "borisyankov/DefinitelyTyped",
        "ref": "master",
        "path": "typings",
        "bundle": "typings/tsd.d.ts",
        "installed": {
            "jquery/jquery.d.ts": {
                "commit": "d67c5e3e1a1291ab58dcaace6ce76f69e860d33c"
            }
        }
    }
}"""
