import math

SCREEN_SIZE = width, height = 960, 600

BIRD_NUMBER = 25
PREDATOR_NUMBER = 3

BIRD_COLLISION_RANGE = 40
BIRD_DETECTION_RANGE = 200
BIRD_VISION_ANGLE = math.pi / 2.0
BIRD_MAX_SPEED = 0.2
BIRD_MAX_TURN_ANGLE = 0.03

PREDATOR_COLLISION_RANGE = 40
PREDATOR_DETECTION_RANGE = 200
PREDATOR_VISION_ANGLE = math.pi / 4.0
PREDATOR_MAX_SPEED = 0.3
PREDATOR_MAX_TURN_ANGLE = 0.03

AVOID_WEIGHT = 0.02
MEAN_SPEED_WEIGHT = 1.0
MEAN_POS_WEIGHT = 1.0
FLEE_WEIGHT = 2.0
CHASE_WEIGHT = 2.0


PREDATORS = {1: [3], 2: [3], 3: [4], 4:[]}
