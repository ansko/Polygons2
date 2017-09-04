import math
import numpy as np

from Classes.Options import Options
from Classes.Point import Point
from Classes.Vector import Vector

from functions.utils import decompose


def disksCross(disk1, disk2):
    o = Options()
    epsilon = o.getProperty('roughEpsilon')
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
    # http://mathworld.wolfram.com/Line-PlaneIntersection.html
    # facet of disk2 and top or bottom of disk1
    vtb1 = Vector(bc1, tc1)
    tc2 = disk2.tc()
    bc2 = disk2.bc()
    vtb2 = Vector(bc2, tc2)
    for (x1, x2, x3) in [(c1 + vtb1 / 2,                 # top
                          disk1.facets()[0] + vtb1 / 2,
                          disk1.facets()[1] + vtb1 / 2),
                         (c1 - vtb1 / 2,                 # bottom
                          disk1.facets()[0] - vtb1 / 2,
                          disk1.facets()[1] - vtb1 / 2)]:
        v12 = Vector(x2, x1)
        v32 = Vector(x2, x3)
        for facet in disk2.facets():
            vToFacet = Vector(c2, facet)
            vInFacet = vtb2.vectorMultiply(vToFacet)
            realLength = vInFacet.l()
            needLength = r * math.tan(math.pi / v) 
            vInFacet = vInFacet * (needLength / realLength)
            for (x4, x5) in [(facet + vInFacet + vtb2 / 2, # top edge
                              facet - vInFacet + vtb2 / 2),
                             (facet + vInFacet - vtb2 / 2, # bottom edge
                              facet - vInFacet - vtb2 / 2)]:
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
                if -epsilon < det1 < epsilon or -epsilon < det2 < epsilon :
                    l = ((r / math.cos(math.pi / v))**2 + h**2 / 4)**0.5
                    if Vector(x1, x4).l() < r / math.cos(math.pi / v):
                        return True
                    if Vector(x1, x5).l() < r / math.cos(math.pi / v):
                        return True
                    #return True
                elif det1 * det2 < -epsilon:
                    v45 = Vector(x4, x5)
                    pti = x4 + v45 * abs(det1) / (abs(det1) + abs(det2))
                    if Vector(x1, pti).l() < r:
                        return True
                        
    for facet1 in disk1.facets():
        x1 = facet1
        vToFacet1 = Vector(x1, c1)
        vInFacet1 = vtb1.vectorMultiply(vToFacet1)
        needLength = r * math.tan(math.pi / v)
        realLength = vInFacet1.l()
        vInFacet *= needLength / realLength
        x2 = x1 + vInFacet + vtb1 / 2
        x3 = x1 - vInFacet + vtb1 / 2
        v12 = Vector(x2, x1)
        v32 = Vector(x2, x3)
        for facet2 in disk2.facets():
            vToFacet = Vector(c2, facet)
            vInFacet = vtb2.vectorMultiply(vToFacet)
            realLength = vInFacet.l()
            needLength = r * math.tan(math.pi / v) 
            vInFacet = vInFacet * (needLength / realLength)
            for (x4, x5) in [(facet + vInFacet + vtb2 / 2, # top edge
                              facet - vInFacet + vtb2 / 2),
                             (facet + vInFacet - vtb2 / 2, # bottom edge
                              facet - vInFacet - vtb2 / 2)]:
                v42 = Vector(x4, x2)
                v52 = Vector(x5, x2)
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
                if -epsilon < det1 < epsilon:
                    xi = x4
                    vectori = Vector(x1, xi)
                    cos = (abs(vectori.x() * vtb1.x() + vectori.y() * vtb1.y() + vectori/z() * vtb1/z())) / vectori.l() / vtb1.l()
                    sin = (1 - cos**2)**0.5
                    axelen = cos * vectori.l()
                    norlen = sin * vectori.l()
                    if axelen < (vtb1 / 2).l() and norlen < needLength:
                         return True
                elif -epsilon < det2 < epsilon :
                    xi = x5
                    vectori = Vector(x1, xi)
                    cos = (abs(vectori.x() * vtb1.x() + vectori.y() * vtb1.y() + vectori/z() * vtb1/z())) / vectori.l() / vtb1.l()
                    sin = (1 - cos**2)**0.5
                    axelen = cos * vectori.l()
                    norlen = sin * vectori.l()
                    if axelen < (vtb1 / 2).l() and norlen < needLength:
                         return True
                elif det1 * det2 < -epsilon:
                    xi = x4 + Vector(x4, x5) * (abs(det1)) / (abs(det1) + abs(det2))
                    vectori = Vector(x1, xi)
                    cos = (abs(vectori.x() * vtb1.x() + vectori.y() * vtb1.y() + vectori/z() * vtb1/z())) / vectori.l() / vtb1.l()
                    sin = (1 - cos**2)**0.5
                    axelen = cos * vectori.l()
                    norlen = sin * vectori.l()
                    if axelen < (vtb1 / 2).l() and norlen < needLength:
                         return True
    return False
