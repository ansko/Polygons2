#!/usr/bin/env python3
# coding utf-8

import math
import numpy as np
import random
from datetime import datetime

from Classes.MatricesPrinter import MatricesPrinter
from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinderInTheShell import PolygonCylinderInTheShell
from Classes.PropertiesPrinter import PropertiesPrinter
from Classes.Vector import Vector

from functions.boxCross import boxCross
from functions.boxCrossByDiskInTheShell import boxCrossByDiskInTheShell
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
    matrixString = 'solid matrix = orthobrick(0, 0, 0;'
    matrixString += ' {0}, {0}, {0})'.format(l)
    attempt = 0
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    h = o.getProperty('polygonalDiskThickness')
    while len(pcs) < desiredDisksNumber and attempt < maxAttempts:
        print('Start of attempt {0} ready {1} of {2}'.format(attempt + 1,
                                                             len(pcs),
                                                             desiredDisksNumber))
        attempt += 1
        pc = PolygonCylinderInTheShell(r, h, len(pcs), int(v))
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
        flag = 0
        if boxCrossByDiskInTheShell(pc):
            continue
        for oldPc in pcs:
            if disksCross(oldPc, pc) or diskDiskInTheShellCross(oldPc, pc) or diskDiskInTheShellCross(pc, oldPc):
                flag = 1
                break
        if flag == 0:
            #for oldPc in pcs:
            #    if disksInTheShellCross(oldPc, pc):
            #        oldPc.addNeighbor(pc.number(), True)
            #        pc.addNeighbor(oldPc.number(), False)
            pcs.append(pc)
            matrixString += ' and not polygonalDisk' + str(len(pcs) - 1) + ' and not pdShell' + str(len(pcs) - 1)
        print('End of attempt   {0} ready {1} of {2}'.format(attempt,
                                                           len(pcs),
                                                           desiredDisksNumber))
    matrixString += ';\ntlo matrix -transparent -maxh={0};'.format(maxhMatrix)
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    fillerString = 'solid filler = orthobrick(0, 0, 0;'
    fillerString += ' {0}, {0}, {0})'.format(l)
    shellString = 'solid shell = orthobrick(0, 0, 0;'
    shellString += ' {0}, {0}, {0})'.format(l)
    for i, pc in enumerate(pcs):
        pc.printToCSG(f)
        fillerString += ' and polygonalDisk{0}'.format(i)
        shellString += ' and pdShell{0}'.format(i)
    fillerString += ';\ntlo filler -maxh={0};'.format(maxhFiller)
    shellString += ';\ntlo shell -maxh={0};'.format(maxhShell)
    f.write(matrixString)
    f.write(fillerString)
    f.write(shellString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
    mp = MatricesPrinter(pcs)
    pp = PropertiesPrinter(pcs)
    
mainExfoliation()
