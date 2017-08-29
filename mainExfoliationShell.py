#!/usr/bin/env python3
# coding utf-8

import copy
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
    cellString = 'solid cell = orthobrick(0, 0, 0;'
    cellString += ' {0}, {0}, {0});\n'.format(l)
    matrixString = 'solid matrix = cell and not filler'
    attempt = 0
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    h = o.getProperty('polygonalDiskThickness')
    tmpPcs = []
    while len(pcs) < desiredDisksNumber and attempt < maxAttempts:
        print('Start of attempt {0} ready {1} of {2}'.format(attempt + 1,
                                                             len(pcs),
                                                             desiredDisksNumber))
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
        flag = 0
        boxCrossString = boxCrossByDiskInTheShell(pc)
        if boxCrossString != [0, 0, 0, 0, 0, 0]:
            copiedCount = 0
            print('not empty', boxCrossString)
            #print('crossing the box, disk{0}'.format(pc.number()))
            flag = 2
            #pc1.setNumber(int(str(pc1.number()) + '000001'))
            if boxCrossString[0] != 0:
                print(copiedCount)
                print('crosses x=0')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [l, 0, 0, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
            if flag != 1 and boxCrossString[1] != 0:
                print(copiedCount)
                print('crosses y=0')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [0, l, 0, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
            if flag != 1 and boxCrossString[2] != 0:
                print(copiedCount)
                print('crosses z=0')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [0, 0, l, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
            if flag != 1 and boxCrossString[3] != 0:
                print(copiedCount)
                print('crosses x=l')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [-l, 0, 0, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
            if flag != 1 and boxCrossString[4] != 0:
                print(copiedCount)
                print('crosses y=l')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [0, -l, 0, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
            if flag != 1 and boxCrossString[5] != 0:
                print(copiedCount)
                print('crosses z=l')
                tmpPcs.append(copy.copy(pc))
                tmpPcs[-1].setCopied(copiedCount)
                copiedCount += 1
                tmpPcs[-1].changeByMatrix(np.array([
                                             [1, 0, 0, 0],
                                             [0, 1, 0, 0],
                                             [0, 0, 1, 0],
                                             [0, 0, -l, 1]
                                            ]))
                for oldPc in pcs:
                    if disksCross(oldPc, pc) or disksCross(oldPc, tmpPcs[-1]):
                        tmpPcs.pop(-1)
                        copiedCount -= 1
                        flag = 1
                        break
        if flag != 1:
            for oldPc in pcs:
                if disksCross(oldPc, pc) or diskDiskInTheShellCross(oldPc, pc) or diskDiskInTheShellCross(pc, oldPc):
                    flag = 1
                    break
        if flag != 1:
            pcs.append(pc)
            matrixString += ' and not polygonalDisk' + str(pc.number()) + ' and not pdShell' + str(pc.number())
            if flag == 2:
                for pc1 in tmpPcs:
                    pcs.append(pc1)
                    matrixString += ' and not polygonalDisk' + str(pc1.number()) + ' and not pdShell' + str(pc1.number())
                
        print('End of attempt   {0} ready {1} of {2}'.format(attempt,
                                                             len(pcs),
                                                             desiredDisksNumber))
    matrixString += ';\ntlo matrix -transparent -maxh={0};\n'.format(maxhMatrix)
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    f.write(cellString)
    if len(pcs) > 0:
        fillerString = 'solid filler = cell and (polygonalDisk0'
        shellString = 'solid shell = cell and (pdShell0'
        for i, pc in enumerate(pcs):
            pc.printToCSG(f)
            if i == 0:
                continue
            fillerString += ' or polygonalDisk{0}'.format(pc.number())
            shellString += ' or pdShell{0}'.format(pc.number())
        fillerString += ');\ntlo filler -maxh={0};\n'.format(maxhFiller)
        shellString += ');\ntlo shell -maxh={0};\n'.format(maxhShell)
        f.write(fillerString)
        f.write(shellString)
    f.write(matrixString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
    mp = MatricesPrinter(pcs)
    pp = PropertiesPrinter(pcs)
    
mainExfoliation()
