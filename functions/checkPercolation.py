import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from functions.disksInTheShellCross import disksInTheShellCross


def checkPercolation(pcs):
    crossings = [[i] for i in range(len(pcs))]
    for i, pc1 in enumerate(pcs):
        for j, pc2 in enumerate(pcs):
            if i == j:
                continue
            if disksInTheShellCross(pc1, pc2):
                print('crossing, ', i, j)
                crossings[i].append(j)
                crossings[j].append(i)
    l = 1
    for crossing in crossings:
        if len(crossing) > l:
            l = len(crossings)
    for i in range(l):
        for j in range(len(crossings)):
            for k in range(len(crossings[j])):
                if k == 0:
                    continue
                else:
                    for element in crossings[j]:
                        if element not in crossings[crossings[j][k]]:
                            crossings[crossings[j][k]].append(element)
    toPop = []
    for i in range(len(crossings)):
        if len(crossings[i]) == 1:
            toPop.append(i)
    for i in toPop[::-1]:
        crossings.pop(i)
    ranges = [[1000000, -1000000, 1000000, -1000000, 1000000, -1000000] for i in range(len(crossings))]
    for i in range(len(crossings)):
        for element in crossings[i]:
            borders = pcs[element].findBorders()
            if borders[0] < ranges[i][0]:
                ranges[i][0] = borders[0]
            if borders[1] > ranges[i][1]:
                ranges[i][1] = borders[1]
            if borders[2] < ranges[i][2]:
                ranges[i][2] = borders[2]
            if borders[3] > ranges[i][3]:
                ranges[i][3] = borders[3]
            if borders[4] < ranges[i][4]:
                ranges[i][4] = borders[4]
            if borders[5] > ranges[i][5]:
                ranges[i][5] = borders[5]
    for delta in ranges:
        if delta[1] - delta[0] > l:
            print('perrcolation along x')
        if delta[3] - delta[2] > l:
            print('perrcolation along y')
        if delta[5] - delta[4] > l:
            print('perrcolation along z')