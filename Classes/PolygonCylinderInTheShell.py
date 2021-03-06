import math
import numpy as np

from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinder import PolygonCylinder
from Classes.Vector import Vector

class PolygonCylinderInTheShell(PolygonCylinder):
    def __init__(self, r, h, num=0, v=16):
        super().__init__(r, h, num, v)
        self.values['neighborsIAmMainWith'] = []
        self.values['neighborsAreMainWithMe'] = []
        
    def __copy__(self):
        copy = PolygonCylinderInTheShell(self.r(), self.h(),
                                         self.number(), len(self.facets()))
        for transformation in self.transformationHistory():
            copy.changeByMatrix(transformation)
        return copy
        
    def addNeighbor(self, number, meIsMain=True):
        if meIsMain:
            self.values['neighborsIAmMainWith'].append(number)
        else:
            self.values['neighborsAreMainWithMe'].append(number)

    def printToCSG(self, f):
        o = Options()
        l = o.getProperty('cubeEdgeLength')
        h = 0.01
        cellString = ' and plane(0, 0, {0}; 0, 0, {0})'.format(l - h)
        cellString += ' and plane(0, {0}, 0; 0, {0}, 0)'.format(l - h)
        cellString += ' and plane({0}, 0, 0; {0}, 0, 0)'.format(l - h)
        cellString += ' and plane({1}, {1}, {1}; 0, 0, -{0})'.format(l - h, h)
        cellString += ' and plane({1}, {1}, {1}; 0, -{0}, 0)'.format(l - h, h)
        cellString += ' and plane({1}, {1}, {1}; -{0}, 0, 0)'.format(l - h, h)
        h = o.getProperty('polygonalDiskThickness')
        maxhFiller = o.getProperty('maxh_f')
        st = 'solid polygonalDisk{3} = plane({0}, {1}, {2}; '
        f.write(st.format(self.values['topCenter'].x(),
                          self.values['topCenter'].y(),
                          self.values['topCenter'].z(),
                          self.number()))
        dx = self.values['topCenter'].x() - self.values['botCenter'].x()
        dy = self.values['topCenter'].y() - self.values['botCenter'].y()
        dz = self.values['topCenter'].z() - self.values['botCenter'].z()
        f.write('{0}, {1}, {2}) '.format(dx,
                                         dy,
                                         dz))
        st = 'and plane({0}, {1}, {2}; '
        f.write(st.format(self.values['botCenter'].x(),
                          self.values['botCenter'].y(),
                          self.values['botCenter'].z()))
        dx = -self.values['topCenter'].x() + self.values['botCenter'].x()
        dy = -self.values['topCenter'].y() + self.values['botCenter'].y()
        dz = -self.values['topCenter'].z() + self.values['botCenter'].z()
        f.write('{0}, {1}, {2})'.format(dx,
                                        dy,
                                        dz))
        for facet in self.values['facets']:
            f.write(' and plane({0}, {1}, {2}; '.format(facet.x(),
                                                        facet.y(),
                                                        facet.z()))
            c = self.c()
            dfc = facet - c
            f.write('{0}, {1}, {2})'.format(dfc.x(), dfc.y(), dfc.z()))
        f.write(cellString)
        f.write(';\n')
        s = o.getProperty('shellThickness')
        v = Vector(self.bc(), self.tc())
        v = v * (2 * s + h) / 2 / h
        pt = self.bc()/2 + self.tc()/2 + v
        st = 'solid pdShell{0} = plane({1}, {2}, {3}; '
        f.write(st.format(self.number(),
                          pt.x(),
                          pt.y(),
                          pt.z()))
        f.write('{0}, {1}, {2}) '.format(v.x(),
                                         v.y(),
                                         v.z()))
        pt = self.bc()/2 + self.tc()/2 - v
        f.write('and plane({1}, {2}, {3}; '.format(self.number(),
                                                   pt.x(),
                                                   pt.y(),
                                                   pt.z()))
        f.write('{0}, {1}, {2}) '.format(-v.x(),
                                         -v.y(),
                                         -v.z()))
        for facet in self.values['facets']:
            vToFacet = Vector(self.c(), facet)
            l = vToFacet.l()
            vToFacet = vToFacet * ((l + s) / l)
            f.write(' and plane({0}, {1}, {2}; '.format(c.x() + vToFacet.x(),
                                                        c.y() + vToFacet.y(),
                                                        c.z() + vToFacet.z()))
            f.write('{0}, {1}, {2})'.format(vToFacet.x(),
                                            vToFacet.y(), vToFacet.z()))
        f.write(cellString)
        f.write(';\n')

    def findBorders(self):
        o = Options()
        minx = miny = minz = 1000000
        maxx = maxy = maxz = -1000000
        s = o.getProperty('shellThickness')
        c = self.c()
        for facet in self.values['facets']:
            vToFacet = Vector(self.c(), facet)
            l = vToFacet.l()
            vToFacet = vToFacet * ((l + s) / l)
            realFacet = c + vToFacet
            if realFacet.x() < minx:
                minx = realFacet.x()
            if realFacet.x() > maxx:
                maxx = realFacet.x()
            if realFacet.y() < miny:
                miny = realFacet.y()
            if realFacet.y() > maxy:
                maxy = realFacet.y()
            if realFacet.z() < minz:
                minz = realFacet.z()
            if realFacet.z() > maxz:
                maxz = realFacet.z()
        return [minx, maxx, miny, maxy, minz, maxz]
