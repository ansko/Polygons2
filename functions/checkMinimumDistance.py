from Classes.Vector import Vector


def checkMinimumDistance(disk1, disk2):
    rMin = 1000000
    for facet1 in disk1.facets():
        for facet2 in disk2.facets():
            length = Vector(facet1, facet2).l()
            if length < rMin:
                rMin = length
    return rMin
