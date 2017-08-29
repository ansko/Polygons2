import math
import numpy as np

from Classes.Options import Options
from Classes.Point import Point


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
        self.values['transformationHistory'] = []
        self.values['copied'] = 0
        alpha = 2 * math.pi / v # angle the vertex is seen from center
        for i in range(v):
            facet = Point(r * math.cos(alpha * i), r * math.sin(alpha * i), 0)
            self.values['facets'].append(facet)
            
    def __copy__(self):
        copy = PolygonCylinder(self.r(), self.h(), self.number(), len(self.facets()))
        for transformation in self.transformationHistory():
            copy.changeByMatrix(transformation)
        return copy
        
    def __str__(self):
        return '{0} {1} {2} r={3} h={4}'.format(self.c().x(), self.c().y(), self.c().z(), self.r(), self.h())
        
    def setCopied(self, number):
        self.values['copied'] = number

    def tc(self):
        return self.values['topCenter']

    def bc(self):
        return self.values['botCenter']

    def c(self):
        return self.bc() / 2 + self.tc() / 2

    def r(self):
        return self.values['r']

    def h(self):
        return self.values['h']
        
    def number(self):
        responce = '0' * self.values['copied']
        responce += str(self.values['number'])
        return responce
        
    def setNumber(self, number):
        self.values['number'] = number
        
    def facets(self):
        return self.values['facets']
        
    def transformationHistory(self):
        return self.values['transformationHistory']
        
    def changeByMatrix(self, M):
        self.values['transformationHistory'].append(M)
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
        o = Options()
        maxhFiller = o.getProperty('maxh_f')
        f.write('solid polygonalDisk{3} = plane({0}, {1}, {2}; '.format(self.values['topCenter'].x(),
                                                                        self.values['topCenter'].y(),
                                                                        self.values['topCenter'].z(),
                                                                        self.number()))
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
            dfc = facet - c
            f.write('{0}, {1}, {2})'.format(dfc.x(), dfc.y(), dfc.z()))
        #f.write(';\ntlo polygonalDisk{0} -maxh={1};\n'.format(self.number(),
        #                                                      maxhFiller))
        f.write(';\n')
