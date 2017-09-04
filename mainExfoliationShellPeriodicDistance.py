#!/usr/bin/env python3
# coding utf-8

import cProfile

import copy
import math
import numpy as np
import random
from datetime import datetime

import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

from Classes.MatricesPrinter import MatricesPrinter
from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinderInTheShell import PolygonCylinderInTheShell
from Classes.PropertiesPrinter import PropertiesPrinter
from Classes.Vector import Vector

from functions.boxCross import boxCross
from functions.boxCrossByDiskInTheShell import boxCrossByDiskInTheShell
from functions.checkMinimumDistance import checkMinimumDistance
from functions.checkPercolation import checkPercolation
from functions.diskDiskInTheShellCross import diskDiskInTheShellCross
from functions.disksCross import disksCross
from functions.disksInTheShellCross import disksInTheShellCross


def mainExfoliation():
    o = Options()
    maxhMatrix = o.getProperty('maxh_m')
    maxhFiller = o.getProperty('maxh_f')
    maxhShell = o.getProperty('maxh_sh')
    desiredDisksNumber = int(o.getProperty('numberOfDisks'))
    maxAttempts = o.getProperty('maxAttempts')
    pcs = []
    l = o.getProperty('cubeEdgeLength')
    #cellString = 'solid cell = orthobrick(0, 0, 0;'
    #cellString += ' {0}, {0}, {0});\n'.format(l)
    cellString = 'solid cell = plane(0, 0, {0}; 0, 0, {0})'.format(l)
    cellString += ' and plane(0, {0}, 0; 0, {0}, 0)'.format(l)
    cellString += ' and plane({0}, 0, 0; {0}, 0, 0)'.format(l)
    cellString += ' and plane(0, 0, 0; 0, 0, -{0})'.format(l)
    cellString += ' and plane(0, 0, 0; 0, -{0}, 0)'.format(l)
    cellString += ' and plane(0, 0, 0; -{0}, 0, 0);\n'.format(l)
    matrixString = 'solid matrix = cell'
    attempt = 0
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    h = o.getProperty('polygonalDiskThickness')
    ready = 0
    tmpPcs = []
    while ready < desiredDisksNumber and attempt < maxAttempts:
        attempt += 1
        if len(pcs) > 0:
            name = int(pcs[len(pcs) - 1].number()) + 1
            pc = PolygonCylinderInTheShell(r, h, name, int(v))
        else:
            pc = PolygonCylinderInTheShell(r, h, 0, int(v))
        random.seed(datetime.now())
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        # rotate around 0x
        pc.changeByMatrix(np.array([
                                    [1, 0, 0, 0],
                                    [0, math.cos(alpha), -math.sin(alpha), 0],
                                    [0, math.sin(alpha), math.cos(alpha), 0],
                                    [0, 0, 0, 1]
                                   ]))
        # rotate around 0y
        pc.changeByMatrix(np.array([
                                    [math.cos(beta), 0, math.sin(beta), 0],
                                    [0, 1, 0, 0],
                                    [-math.sin(beta), 0, math.cos(beta), 0],
                                    [0, 0, 0, 1]
                                   ]))
        # rotate around 0z
        pc.changeByMatrix(np.array([
                                    [math.cos(gamma), -math.sin(gamma), 0, 0],
                                    [math.sin(gamma), math.cos(gamma), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]
                                   ]))
        # translate into random point of the box
        dx = l * random.random()
        dy = l * random.random()
        dz = l * random.random()
        pc.changeByMatrix(np.array([
                                    [1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [dx, dy, dz, 1]
                                   ]))
        tmpPcs = []
        copiedCount = 0
        pcToCheck = None
        for ix in [-1, 0, 1]:
            for iy in [-1, 0, 1]:
                for iz in [-1, 0, 1]:
                    pc1 = copy.copy(pc)
                    pc1.setCopied(copiedCount)
                    copiedCount += 1
                    pc1.changeByMatrix(np.array([
                                                 [1, 0, 0, 0],
                                                 [0, 1, 0, 0],
                                                 [0, 0, 1, 0],
                                                 [ix * l, iy * l, iz * l, 1]
                                                ]))
                    tmpPcs.append(pc1)
                    if (ix, iy, iz) == (0, 0, 0):
                        pcToCheck = pc1
        flag = 0
        for oldPc in pcs:
            #for pc in tmpPcs:
            #    if disksCross(oldPc, pc) or\
            #       disksCross(pc, oldPc) or\
            #       diskDiskInTheShellCross(oldPc, pc) or\
            #       diskDiskInTheShellCross(pc, oldPc):
            #        flag = 1
            #        break
            if disksCross(oldPc, pc) or\
               disksCross(pc, oldPc) or\
               diskDiskInTheShellCross(oldPc, pc) or\
               diskDiskInTheShellCross(pc, oldPc):
                    flag = 1
                    break
        if flag != 1:
            ready += 1
            for pc in tmpPcs:
                pcs.append(pc)
                
        toPop = []
        for i, pc in enumerate(pcs):
            c = pc.c()
            if not 0 < c.x() < l or not 0 < c.y() < l or not 0 < c.z() < l:
                if not boxCrossByDiskInTheShell(pc):
                    toPop.append(i)
        for i in toPop[::-1]:
            pcs.pop(i)
        s = 'End of attempt   {0} ready {1} of {2}'
        print(s.format(attempt, ready, desiredDisksNumber))
    print('Checking for percolation len is {}'.format(len(pcs)))
    for pc in pcs:
        print(pc)
    checkPercolation(pcs)
    s = ' and not filler and not shell;\ntlo matrix -transparent -maxh={0};\n'
    matrixString += s.format(maxhMatrix)
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    f.write(cellString)
    if len(pcs) > 0:
        aveMinDistance = 0
        minDistance = 1000000
        for pc1 in pcs:
            for pc2 in pcs:
                if pc1 == pc2:
                    continue
                distance = checkMinimumDistance(pc1, pc2)
                if distance < minDistance:
                    minDistance = distance
                aveMinDistance += distance
        aveMinDistance /= len(pcs) * (len(pcs) - 1)
        print('MinDistance = ', minDistance)
        print('AveMinDistance = ', aveMinDistance)
        fillerString = 'solid filler = cell and ('
        shellString = 'solid shell = cell and ('
        for i, pc in enumerate(pcs):
            pc.printToCSG(f)
            if i != 0:
                fillerString += ' or polygonalDisk{0}'.format(pc.number())
                shellString += ' or pdShell{0}'.format(pc.number())
            else:
                fillerString += 'polygonalDisk{0}'.format(pc.number())
                shellString += 'pdShell{0}'.format(pc.number())
        fillerString += ');\ntlo filler -maxh={0};\n'.format(maxhFiller)
        s = ') and not filler;\ntlo shell -maxh={0};\n'
        shellString += s.format(maxhShell)
        f.write(fillerString)
        f.write(shellString)
    f.write(matrixString)
    print('Volume fraction is {}'.format(ready * math.pi * r**2 * h / l**3))
    mp = MatricesPrinter(pcs)
    pp = PropertiesPrinter(pcs)

    
mainExfoliation()
