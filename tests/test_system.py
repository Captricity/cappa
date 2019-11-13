

from .base import VagrantTestCase


class SystemTestCases(VagrantTestCase):

    def test_basic(self):
        self.run_spec('system_basic_spec')

    def test_install_single(self):
        self.install_requirements_file(TEST_INSTALL_SINGLE_REQ_JSON)
        self.run_spec('system_install_single_spec')

    def test_install_multiple(self):
        self.install_requirements_file(TEST_INSTALL_MULTIPLE_REQ_JSON)
        self.run_spec('system_install_multiple_spec')

TEST_INSTALL_SINGLE_REQ_JSON = """{
    "sys": {
        "postgresql-client": null
    }
}"""

TEST_INSTALL_MULTIPLE_REQ_JSON = """{
    "sys": {
        "postgresql-client": null,
        "libpq-dev": null
    }
}"""
