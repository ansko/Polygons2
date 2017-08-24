import math

import Classes
from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector

def boxCross(disk):
    o = Options()
    length = o.getProperty('cubeEdgeLength')
    c = disk.c()
    tc = disk.tc()
    bc = disk.bc()
    r = disk.r()
    h = disk.h()
    v = len(disk.facets())
    vtb = Vector(bc, tc)
    for facet in disk.facets():
        vToFacet = facet - c
        vInFacet = vtb.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = r * math.sin(math.pi / v) 
        vInFacet = vInFacet * (needLength / realLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
        if 0 > x4.x() or 0 > x4.y() or 0 > x4.z() or 0 > x5.x() or 0 > x5.y() or 0 > x5.z():
            return True
        if x4.x() > length or x4.y() > length or x4.z() > length or x5.x() > length or x5.y() > length or x5.z() > length:
            return True
    return False