#!/usr/bin/env python3
# coding utf-8

import numpy as np
import math
import random


class Point():
    def __init__(self, x, y, z):
        self.values = dict()
        self.values['x'] = x
        self.values['y'] = y
        self.values['z'] = z

    def __add__(self, otherPoint):
        return Point(self.x() + otherPoint.x(), 
                     self.y() + otherPoint.y(),
                     self.z() + otherPoint.z())

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.x(), self.y(), self.z())

    def x(self):
        return self.values['x']

    def y(self):
        return self.values['y']

    def z(self):
        return self.values['z']


class PolygonCylinder():
    def __init__(self, r, h, num=0, v=16):
        self.values = dict()
        self.values['r'] = r # radius of the inscribed circle
        self.values['h'] = h # height
        self.values['v'] = v # vertices number
        self.values['number'] = num # disk number, used to identify it ('name')
        self.values['topCenter'] = Point(0, 0, h/2)
        self.values['botCenter'] = Point(0, 0, -h/2)
        self.values['facets'] = []
        alpha = 2 * math.pi / v # angle the vertex is seen from center
        for i in range(v):
            facet = Point(r * math.cos(alpha * i), r * math.sin(alpha * i), 0)
            self.values['facets'].append(facet)

    def tc(self):
        return self.values['topCenter']

    def bc(self):
        return self.values['botCenter']

    def c(self):
        return Point(self.values['topCenter'].x()/2 + self.values['botCenter'].x()/2,
                     self.values['topCenter'].y()/2 + self.values['botCenter'].y()/2,
                     self.values['topCenter'].z()/2 + self.values['botCenter'].z()/2)

    def r(self):
        return self.values['r']

    def h(self):
        return self.values['h']

    def facets(self):
        return self.values['facets']
        
    def changeByMatrix(self, M):
        pt = self.values['topCenter']
        pt = np.array([pt.x(), pt.y(), pt.z(), 1])
        pt = np.dot(pt, M)
        self.values['topCenter'] = Point(pt[0], pt[1], pt[2])
        pt = self.values['botCenter']
        pt = np.array([pt.x(), pt.y(), pt.z(), 1])
        pt = np.dot(pt, M)
        self.values['botCenter'] = Point(pt[0], pt[1], pt[2])
        for i in range(len(self.values['facets'])):
            pt = np.array([self.values['facets'][i].x(),
                           self.values['facets'][i].y(),
                           self.values['facets'][i].z(), 1])
            pt = np.dot(pt, M)
            self.values['facets'][i] = Point(pt[0], pt[1], pt[2])

    def printToCSG(self, f):
        f.write('solid polygonalDisk{3} = plane({0}, {1}, {2}; '.format(self.values['topCenter'].x(),
                                                                       self.values['topCenter'].y(),
                                                                       self.values['topCenter'].z(),
                                                                       self.values['number']))
        f.write('{0}, {1}, {2}) '.format(self.values['topCenter'].x() - self.values['botCenter'].x(),
                                         self.values['topCenter'].y() - self.values['botCenter'].y(),
                                         self.values['topCenter'].z() - self.values['botCenter'].z()))
        f.write('and plane({0}, {1}, {2}; '.format(self.values['botCenter'].x(),
                                                   self.values['botCenter'].y(),
                                                   self.values['botCenter'].z()))
        f.write('{0}, {1}, {2})'.format(-self.values['topCenter'].x() + self.values['botCenter'].x(),
                                        -self.values['topCenter'].y() + self.values['botCenter'].y(),
                                        -self.values['topCenter'].z() + self.values['botCenter'].z()))
        for facet in self.values['facets']:
            f.write(' and plane({0}, {1}, {2}; '.format(facet.x(),
                                                        facet.y(),
                                                        facet.z()))
            c = self.c()
            f.write('{0}, {1}, {2})'.format(facet.x() - c.x(),
                                            facet.y() - c.y(),
                                            facet.z() - c.z()))
        #f.write(';\ntlo polygonalDisk{0} -transparent;\n'.format(self.values['number']))
        f.write(';\ntlo polygonalDisk{0};\n'.format(self.values['number']))


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
            return True
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
           
                   
class Options():
    def __init__(self):
        self.values = {}
        self.values['cubeEdgeLength'] = 5

    def getProperty(self, key):
        return self.values[key]
    

def mainExfoliation():
    o = Options()
    f = open('1.geo', 'w')
    f.write('algebraic3d\n')
    pcs = []
    l = o.getProperty('cubeEdgeLength')
    matrixString = 'solid matrix = orthobrick(0, 0, 0; {0}, {0}, {0})'.format(l, l, l)
    attempt = 0
    r = 0.5
    h = 0.1
    while len(pcs) < 1000 and attempt < 200000:
        print('attempt {0} ready {1} of {2}'.format(attempt, len(pcs), 100))
        attempt += 1
        pc = PolygonCylinder(r, h, len(pcs))
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        pc.changeByMatrix(np.array([
                                    [1, 0, 0, 0],
                                    [0, math.cos(alpha), -math.sin(alpha), 0],
                                    [0, math.sin(alpha), math.cos(alpha), 0],
                                    [0, 0, 0, 1]
                                   ]))
        pc.changeByMatrix(np.array([
                                    [math.cos(beta), 0, math.sin(beta), 0],
                                    [0, 1, 0, 0],
                                    [-math.sin(beta), 0, math.cos(beta), 0],
                                    [0, 0, 0, 1]
                                   ]))
        pc.changeByMatrix(np.array([
                                    [math.cos(gamma), -math.sin(gamma), 0, 0],
                                    [math.sin(gamma), math.cos(gamma), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]
                                   ]))
        pc.changeByMatrix(np.array([
                                    [1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [l * random.random(), l * random.random(), l * random.random(), 1]
                                   ]))
        flag = 0
        if boxCross(pc):
            continue
        for oldPc in pcs:
            if disksCross(oldPc, pc):
                flag = 1
        if flag == 0:
            pcs.append(pc)
            matrixString += ' and not polygonalDisk' + str(len(pcs) - 1)
    matrixString += ';\ntlo matrix -transparent;'
    for pc in pcs:
        pc.printToCSG(f)
    f.write(matrixString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
mainExfoliation()
