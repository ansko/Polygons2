from Classes.Point import Point


class Vector(Point):
    def __init__(self, begin, end):
        self.values = dict()
        self.values['begin'] = begin
        self.values['end'] = end
        
    def x(self):
        return self.values['end'].x() - self.values['begin'].x()

    def y(self):
        return self.values['end'].y() - self.values['begin'].y()

    def z(self):
        return self.values['end'].z() - self.values['begin'].z()

    def vectorMultiply(self, otherVector):
        x = self.y() * otherVector.z() - self.z() * otherVector.y()
        y = self.x() * otherVector.z() - self.z() * otherVector.x()
        z = self.x() * otherVector.y() - self.y() * otherVector.x()
        return Vector(Point(0, 0, 0), Point(x, -y, z))
        
    def scalarMultiply(self, otherVector):
        return (self.x() * otherVector.x() +
                self.y() * otherVector.y() + 
                self.z() * otherVector.z())
