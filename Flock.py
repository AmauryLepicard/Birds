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

    def updateSpeeds(self):
        for b in self.birdList:
            self.computeSpeed(b)

    def updatePos(self, deltaTime):
        for b in self.birdList:
            b.position = (b.position + b.speed * deltaTime) % Point(self.w, self.h)

    def computeSpeed(self, bird):
        avoidSpeed = []
        meanSpeed = []
        meanPosSpeed = []
        fleeSpeed = []
        chaseSpeed = []
        newSpeed = False
        for other in self.birdList:
            if (bird != other):
                if (bird.dist(other)) < bird.collisionrange:
                    newSpeed = True
                    avoidSpeed.append((bird.position - other.position) * (2 * bird.collisionrange - bird.dist(other)))
                else:
                    seen, dist = bird.sees(other, bird.visionangle)
                    if seen and dist < bird.detectionrange:
                        newSpeed = True
                        if bird.race == other.race:
                            meanSpeed.append(other.speed)
                            relativePos = other.position - bird.position
                            meanPosSpeed.append(relativePos)
                        if bird.race < other.race:
                            fleeSpeed.append((bird.position - other.position) * (2 * bird.collisionrange - bird.dist(other)))
                        if bird.race > other.race:
                            relativePos = other.position - bird.position
                            chaseSpeed.append(relativePos)

        if (newSpeed):
            #print "new heading", len(avoidSpeed), len(meanSpeed), len(meanPosSpeed)
            newSpeedVector = self.mean(avoidSpeed) * param.AVOID_WEIGHT
            newSpeedVector += self.mean(meanSpeed) * param.MEAN_SPEED_WEIGHT
            newSpeedVector += self.mean(meanPosSpeed) * param.MEAN_POS_WEIGHT
            newSpeedVector += self.mean(fleeSpeed) * param.FLEE_WEIGHT
            newSpeedVector += self.mean(chaseSpeed) * param.CHASE_WEIGHT
            newAngle = math.degrees(math.atan2(newSpeedVector.y, newSpeedVector.x))
            angleDelta = newAngle - bird.getAngle()
            if math.fabs(angleDelta) > bird.maxTurnSpeed:
                correctedAngle = bird.getAngle()
                if bird.getAngle() < newAngle:
                    correctedAngle += bird.maxTurnSpeed
                if bird.getAngle() > newAngle:
                    correctedAngle -= bird.maxTurnSpeed
                newSpeedVector = Point(math.cos(math.radians(correctedAngle)), math.sin(math.radians(correctedAngle))) * abs(newSpeedVector)

            if abs(newSpeedVector) > bird.maxSpeed:
                newSpeedVector = newSpeedVector.normalized() * bird.maxSpeed

            bird.speed = newSpeedVector
            if len(fleeSpeed) != 0:
                bird.state = Bird.FLEEING
            else:
                bird.state = Bird.FOLLOWING
        else:
            heading = math.degrees(math.atan2(bird.speed.y, bird.speed.x))
            heading += random.uniform(-15.0,15.0)
            bird.speed = Point(math.cos(math.radians(heading)),math.sin(math.radians(heading))) * abs(bird.speed)
            bird.state = Bird.FREE

    def mean(self, pointList):
        if len(pointList) != 0:
            m = Point(0, 0)
            for p in pointList:
                m = m + p
            m.div(len(pointList))
            return m
        return Point(0, 0)

