class Point():
    def __init__(self, x, y, z):
        self.values = dict()
        self.values['x'] = x
        self.values['y'] = y
        self.values['z'] = z

    def __add__(self, otherPoint):
        return Point(self.x() + otherPoint.x(), 
                     self.y() + otherPoint.y(),
                     self.z() + otherPoint.z())
                     
    def _radd__(self, otherPoint):
        return Point(self.x() + otherPoint.x(), 
                     self.y() + otherPoint.y(),
                     self.z() + otherPoint.z())
                     
    def __sub__(self, otherPoint):
        return Point(self.x() - otherPoint.x(),
                     self.y() - otherPoint.y(),
                     self.z() - otherPoint.z())
                     
    def __mul__(self, coefficient):
        return Point(self.x() * coefficient,
                     self.y() * coefficient,
                     self.z() * coefficient)
                     
    def __truediv__(self, coefficient):
        return Point(self.x() / coefficient,
                     self.y() / coefficient,
                     self.z() / coefficient)

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.x(), self.y(), self.z())

    def x(self):
        return self.values['x']

    def y(self):
        return self.values['y']

    def z(self):
        return self.values['z']

    def l(self):
        return (self.x()**2 + self.y()**2 + self.z()**2)**0.5