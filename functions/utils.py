import copy
import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from Classes.Options import Options


def delta(i, j):
    if i == j:
        return 1
    return 0


def orderParameter(cosTheta):
    return (3 * cosTheta**2 - 1) / 2
