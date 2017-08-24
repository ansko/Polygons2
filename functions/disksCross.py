import math
import numpy as np

import Classes
from Classes.Point import Point


def disksCross(disk1, disk2):
    c1 = disk1.c()
    tc1 = disk1.tc()
    bc1 = disk1.bc()
    c2 = disk2.c()
    dc12 = c1 - c2
    l = dc12.l()
    r = disk1.r()
    h = disk1.h()
    v = len(disk1.facets())
    if 2 * (r**2 + h**2 / 4)**0.5 < l**0.5:
        return False
    elif h > l:
        return True
    vtb1 = tc1 - bc1
    x1 = c1 + vtb1 / 2
    x2 = disk1.facets()[0] + vtb1 / 2
    x3 = disk1.facets()[1] + vtb1 / 2
    v12 = x1 - x2
    v32 = x3 - x2
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = tc2 - bc2
    for facet in disk2.facets():
        vToFacet = facet - c2
        vInFacet = Point(vtb2.y() * vToFacet.z() - vtb2.z() * vToFacet.y(),
                         -vtb2.x() * vToFacet.z() + vtb2.z() * vToFacet.x(),
                         vtb2.x() * vToFacet.y() - vtb2.y() * vToFacet.x())
        realLength = vInFacet.l()
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / realLength * needLength,
                         vInFacet.y() / realLength * needLength,
                         vInFacet.z() / realLength * needLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
        v42 = x4 - x2
        v52 = x5 - x2
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
        if det1 * det2 < 0:
            return True # why does this work?
                        # why shouldn't i find crossing point and check
                        # whether it belongs to top ot bottom&
    x1 = c1 - vtb1/2
    x2 = disk1.facets()[0] - vtb1 / 2
    x3 = disk1.facets()[1] - vtb1 / 2
    v12 = x1 - x2
    v32 = x3 - x2
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = tc2 - bc2
    for facet in disk2.facets():
        vToFacet = facet - c2
        vInFacet = Point(vtb2.y() * vToFacet.z() - vtb2.z() * vToFacet.y(),
                         -vtb2.x() * vToFacet.z() + vtb2.z() * vToFacet.x(),
                         vtb2.x() * vToFacet.y() - vtb2.y() * vToFacet.x())
        realLength = vInFacet.l()
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / realLength * needLength,
                         vInFacet.y() / realLength * needLength,
                         vInFacet.z() / realLength * needLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
        v42 = x4 - x2
        v52 = x5 - x2
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
        if det1 * det2 < 0:
            return True
    return False