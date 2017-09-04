import math

from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector

def boxCross(disk):
    o = Options()
    additiionalEmptiness = max(o.getProperty('maxh_f'),  # t oavoid errors
                               o.getProperty('maxh_sh'), # in netgen nesh
                               o.getProperty('maxh_m'))  # generation
    length = o.getProperty('cubeEdgeLength')
    c = disk.c()
    tc = disk.tc()
    bc = disk.bc()
    r = disk.r()
    h = disk.h()
    v = len(disk.facets())
    vtb = Vector(bc, tc)
    responce = ''
    for facet in disk.facets():
        vToFacet = facet - c
        vInFacet = vtb.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = r * math.tan(math.pi / v) 
        vInFacet = vInFacet * (needLength / realLength)
        x4 = facet + vInFacet + vtb / 2
        x5 = facet - vInFacet + vtb / 2
        x6 = facet + vInFacet - vtb / 2
        x7 = facet - vInFacet - vtb / 2
        if additiionalEmptiness > x4.x() or x5.x() < additiionalEmptiness:
            return True
        if additiionalEmptiness > x6.x() or x7.x() < additiionalEmptiness:
            return True
        if additiionalEmptiness > x4.y() or x5.y() < additiionalEmptiness:
            return True
        if additiionalEmptiness > x6.y() or x7.y() < additiionalEmptiness:
            return True
        if additiionalEmptiness > x4.z() or x5.z() < additiionalEmptiness:
            return True
        if additiionalEmptiness > x6.z() or x7.z() < additiionalEmptiness:
            return True
        if x4.x() > length - additiionalEmptiness or\
           x5.x() > length - additiionalEmptiness:
            return True
        if x4.y() > length - additiionalEmptiness or\
           x5.y() > length - additiionalEmptiness:
            return True
        if x4.z() > length - additiionalEmptiness or\
           x5.z() > length - additiionalEmptiness:
            return True
        if x6.x() > length - additiionalEmptiness or\
           x7.x() > length - additiionalEmptiness:
            return True
        if x6.y() > length - additiionalEmptiness or\
           x7.y() > length - additiionalEmptiness:
            return True
        if x6.z() > length - additiionalEmptiness or\
           x7.z() > length - additiionalEmptiness:
            return True
    return False
