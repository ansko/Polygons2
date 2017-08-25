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


def mainExfoliationShellCross():
    o = Options()
    maxhMatrix = o.getProperty('maxh_m')
    maxhFiller = o.getProperty('maxh_f')
    maxhShell = o.getProperty('maxh_sh')
    desiredDisksNumber = int(o.getProperty('numberOfDisks'))
    maxAttempts = o.getProperty('maxAttempts')
    pcitss = []
    l = o.getProperty('cubeEdgeLength')
    cellString = 'solid cell = orthobrick(0, 0, 0;'
    cellString += ' {0}, {0}, {0});\n'.format(l)
    matrixString = 'solid matrix = cell'
    attempt = 0
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    h = o.getProperty('polygonalDiskThickness')
    matrixString = 'solid matrix = cell'
    appendedDisksNumber = 0
    while appendedDisksNumber < desiredDisksNumber and attempt < maxAttempts:
        print('Start of attempt {0} ready {1} of {2}'.format(attempt + 1,
                                                             appendedDisksNumber,
                                                             desiredDisksNumber))
        attempt += 1
        pcits = PolygonCylinderInTheShell(r, h, appendedDisksNumber)
        dx = l * random.random()
        dy = l * random.random()
        dz = l * random.random()
        alpha = math.pi * 2 * random.random()
        beta = math.pi * 2 * random.random()
        gamma = math.pi * 2 * random.random()
        # rotate around 0x
        pcits.changeByMatrix(np.array([
                                       [1, 0, 0, 0],
                                       [0, math.cos(alpha), -math.sin(alpha), 0],
                                       [0, math.sin(alpha), math.cos(alpha), 0],
                                       [0, 0, 0, 1]
                                   ]))
        # rotate around 0y
        pcits.changeByMatrix(np.array([
                                       [math.cos(beta), 0, math.sin(beta), 0],
                                       [0, 1, 0, 0],
                                       [-math.sin(beta), 0, math.cos(beta), 0],
                                       [0, 0, 0, 1]
                                   ]))
        # rotate around 0z
        pcits.changeByMatrix(np.array([
                                       [math.cos(gamma), -math.sin(gamma), 0, 0],
                                       [math.sin(gamma), math.cos(gamma), 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]
                                   ]))
        # translate into random point of the box
        pcits.changeByMatrix(np.array([
                                       [1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [dx, dy, dz, 1]
                                   ]))
        boxCrossList = boxCrossByDiskInTheShell(pcits)
        boxCrossingFlag = 0
        if boxCrossList == [0, 0, 0, 0, 0, 0]:
            pass
        else:
            flag_x1 = 0
            flag_x2 = 0
            flag_y1 = 0
            flag_y2 = 0
            flag_z1 = 0
            flag_z2 = 0
            if boxCrossList[0] != 0:
                pcits_x1 = copy.copy(pcits)
                pcits_x1.setCopied(0)
                pcits_x1.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [l, 0, 0, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_x1):
                        flag_x1 = 1
                        break
            if boxCrossList[3] != 0:
                pcits_x2 = copy.copy(pcits)
                pcits_x2.setCopied(1)
                pcits_x2.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [-l, 0, 0, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_x2):
                        flag_x2 = 1
                        break
            if boxCrossList[1] != 0:
                pcits_y1 = copy.copy(pcits)
                pcits_y1.setCopied(2)
                pcits_y1.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [0, l, 0, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_y1):
                        flag_y1 = 1
                        break
            if boxCrossList[4] != 0:
                pcits_y2 = copy.copy(pcits)
                pcits_y2.setCopied(3)
                pcits_y2.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [0, -l, 0, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_y2):
                        flag_y2 = 1
                        break
            if boxCrossList[2] != 0:
                pcits_z1 = copy.copy(pcits)
                pcits_z1.setCopied(4)
                pcits_z1.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [0, 0, l, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_z1):
                        flag_z1 = 1
                        break
            if boxCrossList[5] != 0:
                pcits_z2 = copy.copy(pcits)
                pcits_z2.setCopied(5)
                pcits_z2.changeByMatrix(np.array([
                                                  [1, 0, 0, 0],
                                                  [0, 1, 0, 0],
                                                  [0, 0, 1, 0],
                                                  [0, 0, -l, 1]
                                                 ]))
                for oldPcits in pcitss:
                    if disksCross(oldPcits, pcits_z2):
                        flag_z2 = 1
                        break
        flag = 0
        for oldPcits in pcitss:
            if disksCross(oldPcits, pcits):
                flag = 1
                break
        if [flag, boxCrossingFlag] == [0, 0] or [flag, flag_x1, flag_x2, flag_y1, flag_y2, flag_z1, flag_z2] == [0, 0, 0, 0, 0, 0, 0]:
            pcitss.append(pcits)
            appendedDisksNumber += 1
            if boxCrossList[0] != 0:
                pcitss.append(pcits_x1)
                #appendedDisksNumber += 1
            if boxCrossList[1] != 0:
                pcitss.append(pcits_y1)
                #appendedDisksNumber += 1
            if boxCrossList[2] != 0:
                pcitss.append(pcits_z1)
                #appendedDisksNumber += 1
            if boxCrossList[3] != 0:
                pcitss.append(pcits_x2)
                #appendedDisksNumber += 1
            if boxCrossList[4] != 0:
                pcitss.append(pcits_y2)
                #appendedDisksNumber += 1
            if boxCrossList[5] != 0:
                pcitss.append(pcits_z2)
                #appendedDisksNumber += 1
    cellString = 'solid cell = orthobrick(0, 0, 0;'
    cellString += ' {0}, {0}, {0});\n'.format(l)
    matrixString = 'solid matrix = cell'
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    f.write(cellString)
    if len(pcitss) > 0:
        fillerString = 'solid filler = cell and (polygonalDisk0'
        shellString = 'solid shell = cell and (pdShell0'
        for i, pcits in enumerate(pcitss):
            pcits.printToCSG(f)
            if i == 0:
                continue
            fillerString += ' or polygonalDisk{0}'.format(pcits.number())
            shellString += ' or pdShell{0}'.format(pcits.number())
        fillerString += ');\ntlo filler -maxh={0};\n'.format(maxhFiller)
        shellString += ');\ntlo shell -maxh={0};\n'.format(maxhShell)
        f.write(fillerString)
        f.write(shellString)
    matrixString += ' and not filler and not shell;\ntlo matrix -transparent -maxh={0};\n'.format(maxhMatrix)
    f.write(matrixString)
    print('Volume fraction is {}'.format(appendedDisksNumber * math.pi * r**2 * h / l**3))
            
mainExfoliationShellCross()
