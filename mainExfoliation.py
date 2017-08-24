#!/usr/bin/env python3
# coding utf-8

import math
import numpy as np
import random

import Classes
from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinder import PolygonCylinder

import functions
from functions.boxCross import boxCross
from functions.disksCross import disksCross


def mainExfoliation():
    o = Options()
    desiredDisksNumber = o.getProperty('numberOfDisks')
    maxAttempts = o.getProperty('maxAttempts')
    pcs = []
    l = o.getProperty('cubeEdgeLength')
    matrixString = 'solid matrix = orthobrick(0, 0, 0; {0}, {0}, {0})'.format(l)
    attempt = 0
    r = 0.5
    h = 0.1
    while len(pcs) < desiredDisksNumber and attempt < maxAttempts:
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
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    for pc in pcs:
        pc.printToCSG(f)
    f.write(matrixString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
mainExfoliation()
