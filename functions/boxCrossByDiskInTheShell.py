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
    responce = [0 for i in range(6)]
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
        if 0 > x1.x() or 0 > x2.x() or 0 > x3.x() or 0 > x4.x():
            responce[0] += 1
        if 0 > x1.y() or 0 > x2.y() or 0 > x3.y() or 0 > x4.y():
            responce[1] += 1
        if 0 > x1.z() or 0 > x2.z() or 0 > x3.z() or 0 > x4.z():
            responce[2] += 1
        if length < x1.x() or length < x2.x() or length < x3.x() or length < x4.x():
            responce[3] += 1
        if length < x1.y() or length < x2.y() or length < x3.y() or length < x4.y():
            responce[4] += 1
        if length < x1.z() or length < x2.z() or length < x3.z() or length < x4.z():
            responce[5] += 1
    return responce