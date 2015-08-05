import Bird
import param
from Point import Point
import math, random


class Flock:
    def __init__(self, w, h):
        self.birdList = []
        self.w = w
        self.h = h

    def addBird(self, bird):
        self.birdList.append(bird)

    def updateAccelerations(self, deltaTime):
        for b in self.birdList:
            self.computeAcceleration(b, deltaTime)

    def updatePos(self, deltaTime):
        for b in self.birdList:
            b.speed = (b.speed + b.acceleration * deltaTime)
            if abs(b.speed) > b.maxSpeed:
                b.speed = b.speed.normalized() * b.maxSpeed
            b.position = (b.position + b.speed * deltaTime) % Point(self.w, self.h)

    def computeAcceleration(self, bird, deltaTime):
        avoidAcc = []
        meanAcc = []
        meanPosAcc = []
        fleeAcc = []
        chaseAcc = []
        newAcc = False
        for other in self.birdList:
            if bird != other:
                if bird.dist(other) < bird.collisionrange:
                    newAcc = True
                    avoidAcc.append((bird.position - other.position) * (2 * bird.collisionrange - bird.dist(other)))
                else:
                    seen, dist = bird.sees(other, bird.visionangle)
                    if seen and dist < bird.detectionrange:
                        newAcc = True
                        if bird.race == other.race:
                            meanAcc.append(other.speed)
                            relativePos = other.position - bird.position
                            meanPosAcc.append(relativePos)
                        if bird.race < other.race:
                            fleeAcc.append(
                                (bird.position - other.position) * (2 * bird.collisionrange - bird.dist(other)))
                        if bird.race > other.race:
                            relativePos = other.position - bird.position
                            chaseAcc.append(relativePos)

        if (newAcc):
            # print "new heading", len(avoidAcc), len(meanAcc), len(meanPosSpeed)
            newAccVector = mean(avoidAcc) * param.AVOID_WEIGHT
            newAccVector += mean(meanAcc) * param.MEAN_SPEED_WEIGHT
            newAccVector += mean(meanPosAcc) * param.MEAN_POS_WEIGHT
            newAccVector += mean(fleeAcc) * param.FLEE_WEIGHT
            newAccVector += mean(chaseAcc) * param.CHASE_WEIGHT
            newAngle = math.degrees(math.atan2(newAccVector.y, newAccVector.x))
            angleDelta = newAngle - bird.getAngle()
            if math.fabs(angleDelta) > bird.maxTurnSpeed:
                correctedAngle = bird.getAngle()
                if bird.getAngle() < newAngle:
                    correctedAngle += bird.maxTurnSpeed * deltaTime
                if bird.getAngle() > newAngle:
                    correctedAngle -= bird.maxTurnSpeed * deltaTime
                newAccVector = Point(math.cos(math.radians(correctedAngle)),
                                       math.sin(math.radians(correctedAngle))) * abs(newAccVector)

            if abs(newAccVector) > bird.maxSpeed:
                newAccVector = newAccVector.normalized() * bird.maxSpeed

            bird.acceleration = newAccVector
            if len(fleeAcc) != 0:
                bird.state = Bird.FLEEING
            else:
                bird.state = Bird.FOLLOWING
        else:
            heading = math.degrees(math.atan2(bird.speed.y, bird.speed.x))
            heading += random.uniform(-5.0, 5.0)
            bird.speed = Point(math.cos(math.radians(heading)), math.sin(math.radians(heading))) * abs(bird.speed)
            bird.state = Bird.FREE


def mean(pointList):
    if len(pointList) != 0:
        m = Point(0, 0)
        for p in pointList:
            m = m + p
        m.div(len(pointList))
        return m
    return Point(0, 0)
