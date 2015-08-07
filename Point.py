import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, alpha):
        return Point(self.x * alpha, self.y * alpha)

    def div(self, alpha):
        return Point(self.x / alpha, self.y / alpha)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __abs__(self):
#        print "len", math.sqrt(self.x * self.x + self.y * self.y)
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mod__(self, other):
        return Point(self.x % other.x, self.y % other.y)

    def dist(self, other):
        return abs(self - other)

    def normalize(self):
#        print "normalize", self, type(self), abs(self),
        l = abs(self)
#        print l
#        print type(l), type(self.x), type(self.y)
        self.x = self.x / l
        self.y = self.y / l

    def normalized(self):
        l = abs(self)
        return Point(self.x / l, self.y / l)

    def getTuple(self):
        return int(self.x), int(self.y)
