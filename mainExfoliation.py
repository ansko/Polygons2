#!/usr/bin/env python3
# coding utf-8

import math
import numpy as np
import random
from datetime import datetime

import Classes
from Classes.MatricesPrinter import MatricesPrinter
from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinder import PolygonCylinder
from Classes.PropertiesPrinter import PropertiesPrinter
from Classes.Vector import Vector

import functions
from functions.boxCross import boxCross
from functions.disksCross import disksCross


def mainExfoliation():
    o = Options()
    maxhMatrix = o.getProperty('maxh_m')
    desiredDisksNumber = int(o.getProperty('numberOfDisks'))
    maxAttempts = o.getProperty('maxAttempts')
    maxhMatrix = o.getProperty('maxh_m')
    maxhFiller = o.getProperty('maxh_f')
    pcs = []
    l = o.getProperty('cubeEdgeLength')
    attempt = 0
    v = o.getProperty('verticesNumber')
    r = o.getProperty('polygonalDiskRadius')
    h = o.getProperty('polygonalDiskThickness')
    while len(pcs) < desiredDisksNumber and attempt < maxAttempts:
        attempt += 1
        pc = PolygonCylinder(r, h, len(pcs), int(v))
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
        if boxCross(pc):
            continue
        for oldPc in pcs:
            if disksCross(oldPc, pc) or disksCross(pc, oldPc):
                flag = 1
        if flag == 0:
            pcs.append(pc)
        print('End of attempt   {0} ready {1} of {2}'.format(attempt,
                                                           len(pcs),
                                                           desiredDisksNumber))
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    cellString = 'solid cell = plane(0, 0, {0}; 0, 0, {0})'.format(l)
    cellString += ' and plane(0, {0}, 0; 0, {0}, 0)'.format(l)
    cellString += ' and plane({0}, 0, 0; {0}, 0, 0)'.format(l)
    cellString += ' and plane(0, 0, 0; 0, 0, -{0})'.format(l)
    cellString += ' and plane(0, 0, 0; 0, -{0}, 0)'.format(l)
    cellString += ' and plane(0, 0, 0; -{0}, 0, 0);\n'.format(l)
    matrixString = 'solid matrix = cell and not filler'
    f.write(cellString)
    if len(pcs) > 0:
        fillerString = 'solid filler = cell and ('
        for i, pc in enumerate(pcs):
            pc.printToCSG(f)
            if i != 0:
                fillerString += ' or polygonalDisk{0}'.format(pc.number())
            else:
                fillerString += 'polygonalDisk{0}'.format(pc.number())
        fillerString += ');\ntlo filler -maxh={0};\n'.format(maxhFiller)
        f.write(fillerString)
    matrixString += ';\ntlo matrix -transparent -maxh={0};'.format(maxhMatrix)
    f.write(matrixString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
    mp = MatricesPrinter(pcs)
    pp = PropertiesPrinter(pcs)
    
mainExfoliation()
