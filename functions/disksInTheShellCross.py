import math
import numpy as np

from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector


def disksInTheShellCross(disk1, disk2):
    o = Options()
    epsilon = o.getProperty('roughEpsilon')
    s = o.getProperty('shellThickness')
    c1 = disk1.c()
    tc1 = disk1.tc()
    bc1 = disk1.bc()
    c2 = disk2.c()
    dc12 = c1 - c2
    l = dc12.l()
    r = disk1.r()
    h = disk1.h()
    v = len(disk1.facets())
    if 2 * (r**2 + (h / 2 + s)**2)**0.5 < l**0.5:
        return False
    elif h + 2 * s > l:
        return True
    # facet of disk2 and top of disk1
    vtb1 = Vector(bc1, tc1)
    vtb1 = vtb1 * (2 * s + h) / h
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Vector(bc2, tc2)
    vtb2 = vtb2 * (2 * s + h) / h
    for (x1, x2, x3) in [(c1 + vtb1 / 2,                 # top
                          disk1.facets()[0] + vtb1 / 2,
                          disk1.facets()[1] + vtb1 / 2),
                         (c1 - vtb1 / 2,                 # bottom
                          disk1.facets()[0] - vtb1 / 2,
                          disk1.facets()[1] - vtb1 / 2)]:
        if not 0 < x1.x() < l or not 0 < x1.y() < l or not 0 < x1.y() < l:
            continue
        if not 0 < x2.x() < l or not 0 < x2.y() < l or not 0 < x2.y() < l:
            continue
        if not 0 < x3.x() < l or not 0 < x3.y() < l or not 0 < x3.y() < l:
            continue
        v12 = Vector(x2, x1)
        v32 = Vector(x2, x3)
        for facet in disk2.facets():
            vToFacet = Vector(c2, facet)
            vToFacet = vToFacet * (r + s) / r
            vInFacet = vtb2.vectorMultiply(vToFacet)
            realLength = vInFacet.l()
            needLength = (r + s) * math.tan(math.pi / v) 
            vInFacet = vInFacet * (needLength / realLength)
            #for (x4, x5) in [(facet + vInFacet + vtb2 / 2, # top edge
            #                  facet - vInFacet + vtb2 / 2),
            #                 (facet + vInFacet - vtb2 / 2, # bottom edge
            #                  facet - vInFacet - vtb2 / 2)]:
            for (x4, x5) in [(c2 + vToFacet + vInFacet + vtb2 / 2, # top edge
                              c2 + vToFacet - vInFacet + vtb2 / 2),
                             (c2 + vToFacet + vInFacet - vtb2 / 2, # bottom edge
                              c2 + vToFacet - vInFacet - vtb2 / 2)]:
                if not 0 < x4.x() < l or not 0 < x4.y() < l or not 0 < x4.y() < l:
                    continue
                if not 0 < x5.x() < l or not 0 < x5.y() < l or not 0 < x5.y() < l:
                    continue
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
                if -epsilon < det1 < epsilon or -epsilon < det2 < epsilon :
                    l = ((r / math.cos(math.pi / v))**2 + h**2 / 4)**0.5
                    if Vector(x1, x4).l() < r / math.cos(math.pi / v):
                        return True
                    if Vector(x1, x5).l() < r / math.cos(math.pi / v):
                        return True
                else:
                    v45 = Vector(x4, x5)
                    pti = x4 + Vector(x4, x4 + v45 * abs(det1) / (abs(det1) + abs(det2)))
                    if r + s > Vector(x1, pti).l():
                        if 0 < pti.x() < l and 0 < pti.y() < l and 0 < pti.y() < l:
                            return True
    # facet-facet
    for facet1 in disk1.facets():
        vToFacet1 = Vector(c1, facet1)
        vInFacet1 = vtb1.vectorMultiply(vToFacet1)
        realLength1 = vInFacet1.l()
        needLength1 = (r + s) * math.tan(math.pi / v) 
        vInFacet1 = vInFacet1 * (needLength1 / realLength1)
        x1 = c1 + vToFacet1 * (r + s) / r
        x2 = c1 + vToFacet1 * (r + s) / r + vInFacet1 + vtb1 / 2
        x3 = c1 + vToFacet1 * (r + s) / r + vInFacet1 - vtb1 / 2
        if not 0 < x1.x() < l or not 0 < x1.y() < l or not 0 < x1.y() < l:
            continue
        if not 0 < x2.x() < l or not 0 < x2.y() < l or not 0 < x2.y() < l:
            continue
        if not 0 < x3.x() < l or not 0 < x3.y() < l or not 0 < x3.y() < l:
            continue
        v12 = Vector(x2, x1)
        v32 = Vector(x2, x3)
        for facet in disk2.facets():
            vToFacet = Vector(c2, facet)
            vInFacet = vtb2.vectorMultiply(vToFacet)
            realLength = vInFacet.l()
            needLength = (r + s) * math.tan(math.pi / v) 
            vInFacet = vInFacet * (needLength / realLength)
            for (x4, x5) in [(facet + vInFacet + vtb2 / 2, # top edge
                              facet - vInFacet + vtb2 / 2),
                             (facet + vInFacet - vtb2 / 2, # bottom edge
                              facet - vInFacet - vtb2 / 2)]:
                if not 0 < x4.x() < l or not 0 < x4.y() < l or not 0 < x4.y() < l:
                    continue
                if not 0 < x5.x() < l or not 0 < x5.y() < l or not 0 < x5.y() < l:
                    continue
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
                if -epsilon < det1 < epsilon or -epsilon < det2 < epsilon :
                    l = ((r / math.cos(math.pi / v))**2 + h**2 / 4)**0.5
                    if Vector(x1, x4).l() < r / math.cos(math.pi / v):
                        return True
                    if Vector(x1, x5).l() < r / math.cos(math.pi / v):
                        return True
                else:
                    v45 = Vector(x4, x5)
                    pti = x4 + v45 * abs(det1) / (abs(det1) + abs(det2))
                    if Vector(x1, pti).l() < r + s:
                        if 0 < pti.x() < l and 0 < pti.y() < l and 0 < pti.y() < l:
                            return True
    return False
