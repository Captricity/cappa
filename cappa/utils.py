from __future__ import print_function

import sys


def warn(*objs):
    print("WARNING: ", *objs, file=sys.stderr)
