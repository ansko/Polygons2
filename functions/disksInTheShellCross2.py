import math
import numpy as np

from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector


def disksInTheShellCross(disk1, disk2):
    o = Options()
    epsilon = o.getProperty('roughEpsilon')
    s = o.getProperty('shellThickness')
    length = o.getProperty('cubeEdgeLength')
    h = o.getProperty('polygonalDiskThickness')
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    
    c1 = disk1.c()
    c2 = disk2.c()
    
    vtb1 = Vector(disk1.bc(), disk1.tc())
    vtb1 *= (2 * s + h) / h
    vtb2 = Vector(disk2.bc(), disk2.tc())
    vtb2 *= (2 * s + h) / h
    
    # facet of disk2 and top/bottom of disk1:
    for [x1, x2, x3] in [[c1 + vtb1 / 2, disk1.facets()[0] + vtb1 / 2, disk1.facets()[1] + vtb1 / 2],
                         [c1 - vtb1 / 2, disk1.facets()[0] - vtb1 / 2, disk1.facets()[1] - vtb1 / 2]]:
        v12 = Vector(x2, x1)
        v32 = Vector(x2, x3)
        for facet2 in disk2.facets():
            vToFacet = Vector(facet2, c2)
            vToFacet *= (s + r) / r
            vInFacet = vToFacet.vectorMultiply(vtb2)
            realLength = vInFacet.l()
            needLength = (r + s) * math.tan(math.pi / v)
            vInFacet *= needLength / realLength
            for [x4, x5] in [[c2 + vToFacet + vtb2/2 + vInFacet, c2 + vToFacet + vtb2/2 - vInFacet],
                             [c2 + vToFacet - vtb2/2 + vInFacet, c2 + vToFacet - vtb2/2 - vInFacet],
                             [c2 + vToFacet + vtb2/2 + vInFacet, c2 + vToFacet - vtb2/2 + vInFacet],
                             [c2 + vToFacet + vtb2/2 - vInFacet, c2 + vToFacet - vtb2/2 - vInFacet]]:
                v42 = Vector(x2, x4)
                v52 = Vector(x2, x5)
                det1 = np.linalg.det(np.array([
                                               [v12.x(), v12.y(), v12.z()],
                                               [v32.x(), v32.y(), v32.z()],
                                               [v42.x(), v42.y(), v42.z()]
                                              ]))
                det2 = np.linalg.det(np.array([
                                               [v12.x(), v12.y(), v12.z()],
                                               [v32.x(), v32.y(), v32.z()],
                                               [v52.x(), v52.y(), v52.z()]
                                              ]))
                if abs(det1) < epsilon:
                    if Vector(x4, x1).l() < r + s:
                        return True
                elif abs(det2) < epsilon:
                    if Vector(x5, x1).l() < r + s:
                        return True
                elif det1 * det2 < 0:
                    xi = x4 + Vector(x4, x5) * abs(det1) / (abs(det1) + abs(det2))
                    if Vector(x1, xi).l() < r + s:
                        return True
                    
    return False
