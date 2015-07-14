from __future__ import absolute_import

from .base import VagrantTestCase
from tests import assets

class TsdTestCases(VagrantTestCase):

    def test_basic(self):
        self.install_requirements_json(assets.TEST_NECESSARY_PIP_VIRTUALENV)
        self.install_requirements_json_virtualenv(assets.TEST_NECESSARY_NPM_GIT_NODE)
        self.install_requirements_json_virtualenv(TEST_TSD_VERSION_JASON)
        self.run_spec('tsd_install_basic_spec')


TEST_TSD_VERSION_JASON = """{
    "npmg": {
        "tsd": "0.6.0"
    },
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
