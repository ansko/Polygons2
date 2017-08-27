import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from functions.disksInTheShellCross import disksInTheShellCross


def checkPercolation(pcs):
    crossings = []
    for i, pc1 in enumerate(pcs):
        for j, pc2 in enumerate(pcs):
            if i == j:
                continue
            if disksInTheShellCross(pc1, pc2):
                print('crossing, ', i, j)
                for crossing in crossings:
                    if i in crossing:
                        crossing.append(j)
                    elif j in crossing:
                        crossing.append(i)
                    else:
                        crossing.append([i, j])
    pprint(crossings)