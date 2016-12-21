import yaml
import tempfile


class AnsiblePlaybookFactory(list):
    """
    """
    def construct(self, outfile=None):
        base_play = [{
            'hosts': '127.0.0.1',
            'connection': 'local',
            'tasks': self
        }]
        if outfile is None:
            outfile = tempfile.NamedTemporaryFile()
        yaml.dump(base_play, outfile, default_flow_style=False)
