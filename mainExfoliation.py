#!/usr/bin/env python3
# coding utf-8

import math
import numpy as np
import random
from datetime import datetime

import Classes
from Classes.Options import Options
from Classes.Point import Point
from Classes.PolygonCylinder import PolygonCylinder
from Classes.Vector import Vector

import functions
from functions.boxCross import boxCross
from functions.disksCross import disksCross


def mainExfoliation():
    o = Options()
    maxhMatrix = o.getProperty('maxh_m')
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
            if disksCross(oldPc, pc):
                flag = 1
        if flag == 0:
            pcs.append(pc)
            matrixString += ' and not polygonalDisk' + str(len(pcs) - 1)
        print('End of attempt   {0} ready {1} of {2}'.format(attempt,
                                                           len(pcs),
                                                           desiredDisksNumber))
    matrixString += ';\ntlo matrix -transparent -maxh={0};'.format(maxhMatrix)
    f = open(o.getProperty('fname'), 'w')
    f.write('algebraic3d\n')
    for pc in pcs:
        v = Vector(pc.bc, pc.tc)
        
        pc.printToCSG(f)
    f.write(matrixString)
    print('Volume fraction is {}'.format(len(pcs) * math.pi * r**2 * h / l**3))
    
    
mainExfoliation()
