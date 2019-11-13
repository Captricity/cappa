

import sys


def warn(*objs):
    print("WARNING: ", *objs, file=sys.stderr)
