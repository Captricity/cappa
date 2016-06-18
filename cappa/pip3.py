from __future__ import print_function, absolute_import

from .pip import Pip


class Pip3(Pip):

    def __init__(self, *flags):
        super(Pip3, self).__init__(*flags)
        self.name = 'pip3'
        self.friendly_name = 'pip3'
