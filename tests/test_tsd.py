from __future__ import absolute_import

from .base import VagrantTestCase
from tests.dependencies import NPM_DEPENDENCIES, TSD_DEPENDENCIES


class TsdTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(NPM_DEPENDENCIES)
        self.install_requirements_json(TSD_DEPENDENCIES)
        self.install_requirements_json(TEST_TSD_VERSION_JASON)
        self.run_spec('tsd_install_basic_spec')


TEST_TSD_VERSION_JASON = """{
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
