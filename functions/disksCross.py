import math
import numpy as np

import Classes
from Classes.Point import Point
from Classes.Vector import Vector

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
    # facet of disk2 and top of disk1
    vtb1 = Vector(bc1, tc1)
    x1 = c1 + vtb1 / 2
    x2 = disk1.facets()[0] + vtb1 / 2
    x3 = disk1.facets()[1] + vtb1 / 2
    v12 = Vector(x2, x1)
    v32 = Vector(x2, x3)
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Vector(bc2, tc2)
    for facet in disk2.facets():
        vToFacet = Vector(c2, facet)
        vInFacet = vtb2.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = r * math.tan(math.pi / v) 
        vInFacet = vInFacet * (needLength / realLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
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
        if det1 * det2 < 0:
            return True # why does this work?
                        # why shouldn't i find crossing point and check
                        # whether it belongs to top ot bottom&
    # facet of disk2 and bottom of disk1
    x1 = c1 - vtb1/2
    x2 = disk1.facets()[0] - vtb1 / 2
    x3 = disk1.facets()[1] - vtb1 / 2
    v12 = Vector(x2, x1)
    v32 = Vector(x2, x3)
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Vector(bc2, tc2)
    for facet in disk2.facets():
        vToFacet = Vector(c2, facet)
        vInFacet = vtb2.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = r * math.tan(math.pi / v) 
        vInFacet = vInFacet * (needLength / realLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
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
        if det1 * det2 < 0:
            return True
    return False