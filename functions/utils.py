import copy
import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from Classes.Options import Options
from Classes.Vector import Vector


def delta(i, j):
    if i == j:
        return 1
    return 0


def orderParameter(cosTheta):
    return (3 * cosTheta**2 - 1) / 2


def decompose(basis, vector):
    o = Options()
    epsilon = o.getProperty('epsilon')
    axeVector = basis[0]
    basisVector1 = basis[1]
    basisVector2 = basis[2]
    x1 = axeVector.x()
    x2 = basisVector1.x()
    x3 = basisVector2.x()
    y1 = axeVector.y()
    y2 = basisVector1.y()
    y3 = basisVector2.y()
    z1 = axeVector.z()
    z2 = basisVector1.z()
    z3 = basisVector2.z()
    a = vector.x()
    b = vector.y()
    c = vector.z()
    determinant = det([[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]])
    if abs(determinant) < epsilon:
        print('Determinant = ', determinant)
        pprint([[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]])
    alpha = det([[a, x2, x3], [b, y2, y3], [c, z2, z3]]) / determinant
    beta = det([[x1, a, x3], [y1, b, y3], [z1, c, z3]]) / determinant
    gamma = det([[x1, x2, a], [y1, y2, b], [z1, z2, c]]) / determinant
    return [alpha, beta, gamma]