import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from Classes.Options import Options

from functions.disksInTheShellCross2 import disksInTheShellCross


def checkPercolation(pcs):
    """If there is a chain including a particle and its periodic
       image, there is percolation in the system"""
    o = Options()
    crossings = [[i] for i in range(len(pcs))]
    for i in range(len(pcs)):
        for j in range(i + 1, len(pcs)):
            pc1 = pcs[i]
            pc2 = pcs[j]
            if disksInTheShellCross(pc1, pc2):
                print(i, j)
                crossings[i].append(j)
                crossings[j].append(i)
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
            if not i in toPop:
                toPop.append(i)
    for i in toPop[::-1]:
        crossings.pop(i)
    for i, crossing in enumerate(crossings):
        crossings[i] = set(crossing)
    toPop = []
    for i in range(len(crossings)):
        for j in range(i + 1, len(crossings)):
            if crossings[i] - crossings[j] == set():
                if not i in toPop:
                    toPop.append(i)
    print(toPop)
    for i in toPop[::-1]:
        crossings.pop(i)
        
    pprint(crossings)
    
    names = []
    for j, crossing in enumerate(crossings):
        names.append([])
        for i in crossing:
            names[j].append(pcs[i].number())
    for i in range(len(pcs)):
        for namesString in names:
            string1 = str(i)
            for j in range(27):
                string2 = '0' * j + string1
                if string1 in namesString and string2 in namesString:
                    print(percolation)
#    names = []
#    for i in crossings:
#        for j in i:
#            print(int(pcs[j].number()), end=' ')
#        print()
    return None
    
