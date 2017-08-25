import math

from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector

def boxCrossByDiskInTheShell(disk):
    o = Options()
    length = o.getProperty('cubeEdgeLength')
    c = disk.c()
    s = o.getProperty('shellThickness')
    tc = disk.tc()
    bc = disk.bc()
    r = disk.r()
    h = disk.h()
    v = len(disk.facets())
    vtb = Vector(bc, tc)
    vtb = vtb * (2 * s + h) / h
    for facet in disk.facets():
        ptOnFacet = c + (facet - c) / r * (r + s)
        vToFacet = facet - c
        vInFacet = vtb.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = (r + s) * math.tan(math.pi / v)
        vInFacet = vInFacet * (needLength / realLength)
        x1 = ptOnFacet + vInFacet + vtb / 2
        x2 = ptOnFacet + vInFacet - vtb / 2
        x3 = ptOnFacet - vInFacet + vtb / 2
        x4 = ptOnFacet - vInFacet - vtb / 2
        if (0 > x1.x() or 0 > x1.y() or 0 > x1.z() or
            0 > x2.x() or 0 > x2.y() or 0 > x2.z() or
            0 > x3.x() or 0 > x3.y() or 0 > x3.z() or
            0 > x4.x() or 0 > x4.y() or 0 > x4.z()):
            return True
        if (x1.x() > length or x1.y() > length or x1.z() > length or
            x2.x() > length or x2.y() > length or x2.z() > length or
            x3.x() > length or x3.y() > length or x3.z() > length or
            x4.x() > length or x4.y() > length or x4.z() > length):
            return True
    return False
