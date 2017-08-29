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
        ifcrossx = False
        ifcrossy = False
        ifcrossz = False
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
        if x1.x() * x2.x() < 0 or x1.x() * x3.x() < 0 or x1.x() * x4.x() < 0:
            ifcrossx = True
        if (x1.x() - length) * (x2.x() - length) < 0 or\
           (x1.x() - length) * (x3.x() - length) < 0 or\
           (x1.x() - length) * (x4.x() - length) < 0:
            ifcrossx = True
        if x1.y() * x2.y() < 0 or x1.y() * x3.y() < 0 or x1.y() * x4.y() < 0:
            ifcrossy = True
        if (x1.y() - length) * (x2.y() - length) < 0 or\
           (x1.y() - length) * (x3.y() - length) < 0 or\
           (x1.y() - length) * (x4.y() - length) < 0:
            ifcrossy = True
        if x1.z() * x2.z() < 0 or x1.z() * x3.z() < 0 or x1.z() * x4.z() < 0:
            ifcrossz = True
        if (x1.z() - length) * (x2.z() - length) < 0 or\
           (x1.z() - length) * (x3.z() - length) < 0 or\
           (x1.z() - length) * (x4.z() - length) < 0:
            ifcrossz = True
        if ifcrossx and not ifcrossy and not ifcrossz:
            if 0 < c.y() < length and 0 < c.z() < length:
                return True
        if ifcrossy and not ifcrossx and not ifcrossz:
            if 0 < c.x() < length and 0 < c.z() < length:
                return True
        if ifcrossz and not ifcrossy and not ifcrossx:
            if 0 < c.y() < length and 0 < c.x() < length:
                return True
        if ifcrossx and ifcrossy and not ifcrossz:
            if 0 < c.z() < length:
                return True
        if ifcrossx and ifcrossz and not ifcrossy:
            if 0 < c.y() < length:
                return True
        if ifcrossz and ifcrossy and not ifcrossx:
            if 0 < c.x() < length:
                return True
        if ifcrossx and ifcrossy and ifcrossz:
            return True
    return False