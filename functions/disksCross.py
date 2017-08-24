import math
import numpy as np

import Classes
from Classes.Point import Point


def disksCross(disk1, disk2):
    c1 = disk1.c()
    tc1 = disk1.tc()
    bc1 = disk1.bc()
    c2 = disk2.c()
    x = c1.x() - c2.x()
    y = c1.y() - c2.y()
    z = c1.z() - c2.z()
    l = x**2 + y**2 + z**2
    r = disk1.r()
    h = disk1.h()
    v = len(disk1.facets())
    if 2 * (r**2 + h**2 / 4)**0.5 < l**0.5:
        return False
    elif h > l:
        return True
    vtb1 = Point(tc1.x() - bc1.x(), tc1.y() - bc1.y(), tc1.z() - bc1.z())
    x1 = c1 + Point(vtb1.x()/2, vtb1.y()/2, vtb1.z()/2)
    x2 = disk1.facets()[0] + Point(vtb1.x()/2, vtb1.y()/2, vtb1.z()/2)
    x3 = disk1.facets()[1] + Point(vtb1.x()/2, vtb1.y()/2, vtb1.z()/2)
    v12 = Point(x1.x() - x2.x(), x1.y() - x2.y(), x1.z() - x2.z())
    v32 = Point(x3.x() - x2.x(), x3.y() - x2.y(), x3.z() - x2.z())
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Point(tc2.x() - bc2.x(), tc2.y() - bc2.y(), tc2.z() - bc2.z())
    for facet in disk2.facets():
        vToFacet = Point(facet.x() - c2.x(),
                         facet.y() - c2.y(),
                         facet.z() - c2.z())
        vInFacet = Point(vtb2.y() * vToFacet.z() - vtb2.z() * vToFacet.y(),
                         -vtb2.x() * vToFacet.z() + vtb2.z() * vToFacet.x(),
                         vtb2.x() * vToFacet.y() - vtb2.y() * vToFacet.x())
        length = (vInFacet.x()**2 + vInFacet.y()**2 + vInFacet.z()**2)**0.5
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / length * needLength,
                         vInFacet.y() / length * needLength,
                         vInFacet.z() / length * needLength)
        x4 = Point(facet.x() + vInFacet.x(),
                   facet.y() + vInFacet.y(),
                   facet.z() + vInFacet.z())
        x5 = Point(facet.x() - vInFacet.x(),
                   facet.y() - vInFacet.y(),
                   facet.z() - vInFacet.z())
        v42 = Point(x4.x() - x2.x(), x4.y() - x2.y(), x4.z() - x2.z())
        v52 = Point(x5.x() - x2.x(), x5.y() - x2.y(), x5.z() - x2.z())
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
    x1 = c1 + Point(-vtb1.x()/2, -vtb1.y()/2, -vtb1.z()/2)
    x2 = disk1.facets()[0] + Point(-vtb1.x()/2, -vtb1.y()/2, -vtb1.z()/2)
    x3 = disk1.facets()[1] + Point(-vtb1.x()/2, -vtb1.y()/2, -vtb1.z()/2)
    v12 = Point(x1.x() - x2.x(), x1.y() - x2.y(), x1.z() - x2.z())
    v32 = Point(x3.x() - x2.x(), x3.y() - x2.y(), x3.z() - x2.z())
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Point(tc2.x() - bc2.x(), tc2.y() - bc2.y(), tc2.z() - bc2.z())
    for facet in disk2.facets():
        vToFacet = Point(facet.x() - c2.x(),
                         facet.y() - c2.y(),
                         facet.z() - c2.z())
        vInFacet = Point(vtb2.y() * vToFacet.z() - vtb2.z() * vToFacet.y(),
                         -vtb2.x() * vToFacet.z() + vtb2.z() * vToFacet.x(),
                         vtb2.x() * vToFacet.y() - vtb2.y() * vToFacet.x())
        length = (vInFacet.x()**2 + vInFacet.y()**2 + vInFacet.z()**2)**0.5
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / length * needLength,
                         vInFacet.y() / length * needLength,
                         vInFacet.z() / length * needLength)
        x4 = Point(facet.x() + vInFacet.x(),
                   facet.y() + vInFacet.y(),
                   facet.z() + vInFacet.z())
        x5 = Point(facet.x() - vInFacet.x(),
                   facet.y() - vInFacet.y(),
                   facet.z() - vInFacet.z())
        v42 = Point(x4.x() - x2.x(), x4.y() - x2.y(), x4.z() - x2.z())
        v52 = Point(x5.x() - x2.x(), x5.y() - x2.y(), x5.z() - x2.z())
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
