import math

import Classes
from Classes.Options import Options
from Classes.Point import Point

def boxCross(disk):
    o = Options()
    length = o.getProperty('cubeEdgeLength')
    c = disk.c()
    tc = disk.tc()
    bc = disk.bc()
    r = disk.r()
    h = disk.h()
    v = len(disk.facets())
    vtb = Point(tc.x() - bc.x(), tc.y() - bc.y(), tc.z() - bc.z())
    for facet in disk.facets():
        vToFacet = Point(facet.x() - c.x(),
                         facet.y() - c.y(),
                         facet.z() - c.z())
        vInFacet = Point(vtb.y() * vToFacet.z() - vtb.z() * vToFacet.y(),
                         -vtb.x() * vToFacet.z() + vtb.z() * vToFacet.x(),
                         vtb.x() * vToFacet.y() - vtb.y() * vToFacet.x())
        realLength = (vInFacet.x()**2 + vInFacet.y()**2 + vInFacet.z()**2)**0.5
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / realLength * needLength,
                         vInFacet.y() / realLength * needLength,
                         vInFacet.z() / realLength * needLength)
        x4 = Point(facet.x() + vInFacet.x(),
                   facet.y() + vInFacet.y(),
                   facet.z() + vInFacet.z())
        x5 = Point(facet.x() - vInFacet.x(),
                   facet.y() - vInFacet.y(),
                   facet.z() - vInFacet.z())
        if 0 > x4.x() or 0 > x4.y() or 0 > x4.z() or 0 > x5.x() or 0 > x5.y() or 0 > x5.z():
            return True
        if x4.x() > length or x4.y() > length or x4.z() > length or x5.x() > length or x5.y() > length or x5.z() > length:
            return True
    return False
