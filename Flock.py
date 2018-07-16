import Bird
import param
import math
import random
import numpy as np
import pygame


class Flock(pygame.sprite.Group):

    def __init__(self, w, h):
        # Call the parent class (Group) constructor
        pygame.sprite.Group.__init__(self)

        self.birdList = []
        self.w = w
        self.h = h

    def addBird(self, bird):
        self.birdList.append(bird)
        self.add(bird)

    def update(self, deltaTime):
        self.updateAccelerations(deltaTime)
        self.updatePos(deltaTime)
        self.killPreys()

    def killPreys(self):
        for bird in self.birdList:
            for other in self.birdList:
                if bird.race in param.PREDATORS[other.race]:
                    dist = np.linalg.norm(np.array([bird.position[0]-other.position[0], bird.position[1]-other.position[1]]))
                    if dist < 10:
                        self.birdList.remove(other)
                        self.remove(other)

    def updateAccelerations(self, deltaTime):
        for b in self.birdList:
            self.computeAcceleration(b, deltaTime)

    def updatePos(self, deltaTime):
        for b in self.birdList:
            b.speed = (b.speed + b.acceleration * deltaTime)
            if np.linalg.norm(b.speed) > b.maxSpeed:
                b.speed = b.speed / np.linalg.norm(b.speed) * b.maxSpeed
            b.position = (b.position + b.speed * deltaTime) % np.array([self.w, self.h])

            heading = math.atan2(b.speed[1], b.speed[0])

            b.image = pygame.transform.rotozoom(b.baseImage, -heading * 180 / math.pi, 1.0)

            b.image.set_colorkey((0, 0, 0))
            b.rect = b.image.get_rect(center=(b.position[0], b.position[1]))

    def computeAcceleration(self, bird, deltaTime):
        avoidAcc = []
        meanAcc = []
        meanPosAcc = []
        fleeAcc = []
        chaseAcc = []
        newAcc = False
        for other in self.birdList:
            if bird != other:
                relativePos = other.position - bird.position
                dist = bird.dist(other)
                if dist < bird.collisionRange and bird.race not in param.PREDATORS[other.race]:
                    newAcc = True
                    avoidAcc.append(-relativePos * math.pow(bird.collisionRange - dist, 2))
                else:
                    seen = bird.sees(other, bird.visionAngle)
                    if seen and dist < bird.detectionRange:
                        newAcc = True
                        if bird.race == other.race:
                            meanAcc.append(other.speed)
                            meanPosAcc.append(relativePos)
                        if other.race in param.PREDATORS[bird.race]:
                            fleeAcc.append(-relativePos * math.pow(bird.detectionRange - dist, 2))
                        if bird.race in param.PREDATORS[other.race]:
                            chaseAcc.append(relativePos)

        if newAcc:
            # print "new heading", len(avoidAcc), len(meanAcc), len(meanPosSpeed)
            newAccVector = mean(avoidAcc) * param.AVOID_WEIGHT
            newAccVector += mean(meanAcc) * param.MEAN_SPEED_WEIGHT
            newAccVector += mean(meanPosAcc) * param.MEAN_POS_WEIGHT
            newAccVector += mean(fleeAcc) * param.FLEE_WEIGHT
            newAccVector += mean(chaseAcc) * param.CHASE_WEIGHT
            #newAccVector += Point(100.0, 0.0)
            # newAngle = math.degrees(math.atan2(newAccVector.y, newAccVector.x))
            # angleDelta = newAngle - bird.getAngle()
            # if math.fabs(angleDelta) > bird.maxTurnSpeed:
            #     correctedAngle = bird.getAngle()
            #     if bird.getAngle() < newAngle:
            #         correctedAngle += bird.maxTurnSpeed * deltaTime
            #     if bird.getAngle() > newAngle:
            #         correctedAngle -= bird.maxTurnSpeed * deltaTime
            #     newAccVector = Point(math.cos(math.radians(correctedAngle)), math.sin(math.radians(correctedAngle))) * abs(newAccVector)

            bird.acceleration = newAccVector
            heading = math.atan2(bird.speed[1], bird.speed[0])
            if len(fleeAcc) != 0:
                bird.state = Bird.FLEEING
            else:
                bird.state = Bird.FOLLOWING

        else:
            heading = math.atan2(bird.speed[1], bird.speed[0])
            heading *= random.uniform(0.9, 1.1)
            bird.speed = np.array([math.cos(heading), math.sin(heading)]) * abs(bird.speed)
            bird.state = Bird.FREE



def mean(pointList):
    if len(pointList) != 0:
        m = np.zeros(2)
        for p in pointList:
            m = m + p
        m /= len(pointList)
        return m
    return np.zeros(2)
