

from .base import VagrantTestCase


class CappaListTestCase(VagrantTestCase):

    def test_list(self):
        self.install_requirements_file(TEST_FULL_INSTALL_JSON)
        self.run_spec('cappa_list_spec')

TEST_FULL_INSTALL_JSON = """{
    "sys": {
        "python-pip": null,
        "git": null,
        "npm": null,
        "nodejs-legacy": null,
        "fortune": null
    },
    "pip": {
        "delorean": null
    },
    "npm": {
        "lodash": "4.2.1"
    },
    "npmg": {
        "bower": null,
        "nyancat": "0.0.4"
    },
    "bower": {
        "jquery": "2.1.4"
    }
}"""
