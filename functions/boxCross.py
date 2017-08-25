import math

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
    responce = ''
    for facet in disk.facets():
        vToFacet = facet - c
        vInFacet = vtb.vectorMultiply(vToFacet)
        realLength = vInFacet.l()
        needLength = r * math.tan(math.pi / v) 
        vInFacet = vInFacet * (needLength / realLength)
        x4 = facet + vInFacet
        x5 = facet - vInFacet
        if 0 > x4.x() or x5.x() < 0:
            responce += '1'
        else:
            responce += '0'
        if 0 > x4.y() or x5.y() < 0:
            responce += '1'
        else:
            responce += '0'
        if 0 > x4.z() or x5.z():
            responce += '1'
        else:
            responce += '0'
        if x4.x() > length or x5.x() > length:
            responce += '1'
        else:
            responce += '0'
        if x4.y() > length or x5.y() > length:
            responce += '1'
        else:
            responce += '0'
        if x4.z() > length or x5.z() > length:
            responce += '1'
        else:
            responce += '0'
    return responce
