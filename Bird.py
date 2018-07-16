import param
import math
import random
import pygame
import numpy as np

FREE = 0
FOLLOWING = 1
FLEEING = 2


class Bird(pygame.sprite.Sprite):

    def __init__(self, name, c, size, x, y, race, collisionRange, detectionRange, visionAngle, maxspeed):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.name = name
        self.color = c
        self.size = size
        self.position = np.array([x, y])
        angle = random.uniform(0.0, math.pi * 2)
        self.maxSpeed = maxspeed
        self.maxTurnSpeed = param.BIRD_MAX_TURN_ANGLE
        self.speed = np.array([math.cos(angle), math.sin(angle)]) * self.maxSpeed
        self.acceleration = np.array([0.0, 0.0])
        self.state = FREE
        self.race = race
        self.collisionRange = collisionRange
        self.detectionRange = detectionRange
        self.visionAngle = visionAngle

        # baseImage
        self.baseImage = pygame.Surface((self.size * 2, self.size + 1))
        self.baseImage.set_colorkey((0, 0, 0))
        pygame.draw.aalines(self.baseImage, self.color, False, [(0, 0), (self.size * 2, self.size * 0.5), (0, self.size)], 1)
        pygame.draw.aalines(self.baseImage, self.color, False, [(self.size * 0.5, self.size * 0.125), (self.size * 0.5, self.size * 0.875)], 1)

        self.image = self.baseImage
        # generating  rect
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size * 2)
        self.rect.center = (self.position[0], self.position[1])

    def getAngle(self):
        return np.arctan2(self.speed[1], self.speed[0])

    def sees(self, other, angle):
        if abs(np.arctan2(other.position[1] - self.position[1], other.position[0] - self.position[0])) < angle:
            return True
        return False

    def dist(self, other):
        return np.linalg.norm(self.position - other.position)

