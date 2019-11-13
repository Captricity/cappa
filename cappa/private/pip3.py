

import os

from ..pip3 import Pip3


class PrivatePip3(Pip3):

    def __init__(self, org, *flags):
        super(PrivatePip3, self).__init__(*flags)
        self.org = org

    def install(self, packages):
        packages = self._private_package_dict(packages)
        super(PrivatePip3, self).install(packages)

    def _private_package_dict(self, packages):
        def repo_url(repo_string):
            repo_split = repo_string.split('@')
            if len(repo_split) > 1:
                repo, version = repo_split
            else:
                repo = repo_split[0]
                version = 'master'
            if self.private_https_oauth:
                # Use https with oauth. Pulls token from env
                token = os.environ['GITHUB_TOKEN']
                return 'git+https://{}@github.com/{}/{}.git@{}'.format(token, self.org, repo, version)
            else:
                return 'git+ssh://git@github.com/{}/{}.git@{}'.format(self.org, repo, version)

        private_package_dict = {repo_url(repo): None for repo in packages}
        return private_package_dict
