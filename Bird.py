import Point, param
import math, random

FREE = 0
FOLLOWING = 1
FLEEING = 2

class Bird(object):

    def __init__(self, name, c, x, y, race, collisionRange, detectionRange, visionAngle, maxspeed):
        self.name = name
        self.color = c
        self.position = Point.Point(x, y)
        angle = random.uniform(0.0, 360.0)
        self.maxSpeed = maxspeed
        self.maxTurnSpeed = param.BIRD_MAX_TURN_ANGLE
        self.speed = Point.Point(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * self.maxSpeed
        self.acceleration = Point.Point(0.0, 0.0)
        self.state = FREE
        self.race = race
        self.collisionRange = collisionRange
        self.detectionRange = detectionRange
        self.visionAngle = visionAngle

    def getAngle(self):
        return math.degrees(math.atan2(self.speed.y, self.speed.x))

    def sees(self, other, angle):
        if abs(math.degrees(math.atan2(other.position.y - self.position.y, other.position.x - self.position.x))) < angle:
            return True, self.dist(other)
        return False, self.dist(other)

    def dist(self, other):
        return self.position.dist(other.position)