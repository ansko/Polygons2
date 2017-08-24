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
    vtb = tc - bc
    for facet in disk.facets():
        vToFacet = facet - c
        vInFacet = Point(vtb.y() * vToFacet.z() - vtb.z() * vToFacet.y(),
                         -vtb.x() * vToFacet.z() + vtb.z() * vToFacet.x(),
                         vtb.x() * vToFacet.y() - vtb.y() * vToFacet.x())
        realLength = vInFacet.l()
        needLength = r * math.sin(math.pi / v) 
        vInFacet = Point(vInFacet.x() / realLength * needLength,
                         vInFacet.y() / realLength * needLength,
                         vInFacet.z() / realLength * needLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
        if 0 > x4.x() or 0 > x4.y() or 0 > x4.z() or 0 > x5.x() or 0 > x5.y() or 0 > x5.z():
            return True
        if x4.x() > length or x4.y() > length or x4.z() > length or x5.x() > length or x5.y() > length or x5.z() > length:
            return True
    return False