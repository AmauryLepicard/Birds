import pygame, sys, param, random
from Flock import Flock
import Point
import Bird

pygame.init()
screen = pygame.display.set_mode(param.SCREEN_SIZE)
myFont = pygame.font.SysFont(None, 15)

birdFollowingImage = pygame.image.load("bird-following.png")
birdFreeImage = pygame.image.load("bird-free.png")
birdFleeingImage = pygame.image.load("bird-fleeing.png")
predatorImage = pygame.image.load("predator.png")

myFlock = Flock(param.SCREEN_SIZE[0], param.SCREEN_SIZE[1])
for i in range(param.BIRD_NUMBER):
    myFlock.addBird(Bird.Bird("bird" + str(i), (0, 0, 0), random.uniform(0, param.SCREEN_SIZE[0]), random.uniform(0, param.SCREEN_SIZE[1]), 1, param.BIRD_COLLISION_RANGE, param.BIRD_DETECTION_RANGE, param.BIRD_VISIONANGLE, param.BIRD_MAX_SPEED))
for i in range(param.PREDATOR_NUMBER):
    predator = Bird.Bird("predator" + str(i), (0, 0, 0), random.uniform(0, param.SCREEN_SIZE[0]), random.uniform(0, param.SCREEN_SIZE[1]), 2, param.PREDATOR_COLLISION_RANGE, param.PREDATOR_DETECTION_RANGE, param.PREDATOR_VISION_ANGLE, param.BIRD_MAX_SPEED * 1.1)
    myFlock.addBird(predator)

mousePredator = Bird.Bird("mouse", (0, 0, 0), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, param.PREDATOR_COLLISION_RANGE, param.PREDATOR_DETECTION_RANGE, param.PREDATOR_VISION_ANGLE,0.0)
mousePredator.maxTurnSpeed = 0.0
myFlock.addBird(mousePredator)

myClock = pygame.time.Clock()
cpt = 0
showRadius = False
while 1:
    deltaTime = myClock.tick(60)
    cpt += 1
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_a):
            print("exiting...")
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            showRadius = not showRadius
    mousePredator.position = Point.Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    myFlock.updateAccelerations(deltaTime)
    myFlock.updatePos(deltaTime)
    for b in myFlock.birdList:
        tmpImage = pygame.transform.rotate(birdFollowingImage, -b.getAngle())
        if b.state == Bird.FOLLOWING:
            tmpImage = pygame.transform.rotate(birdFollowingImage, -b.getAngle())
            tmpImage = pygame.transform.scale(tmpImage, (16, 16))
        if b.state == Bird.FLEEING:
            tmpImage = pygame.transform.rotate(birdFleeingImage, -b.getAngle())
            tmpImage = pygame.transform.scale(tmpImage, (16, 16))
        if b.state == Bird.FREE:
            tmpImage = pygame.transform.rotate(birdFreeImage, -b.getAngle())
            tmpImage = pygame.transform.scale(tmpImage, (16, 16))
        if b.race == 2:
            tmpImage = pygame.transform.rotate(predatorImage, -b.getAngle())
        if b.race != 3:
            screen.blit(tmpImage,
                        pygame.Rect(b.position.x - tmpImage.get_width() / 2, b.position.y - tmpImage.get_height() / 2,
                                    0, 0))
        if showRadius:
            pygame.draw.circle(screen, (0, 255, 0), b.position.getTuple(), b.collisionRange, 1)
            pygame.draw.circle(screen, (0, 0, 255), b.position.getTuple(), b.detectionRange, 1)
            # pygame.draw.line(screen, (255, 255, 255), b.position.getTuple(), (b.position + b.speed * 50.0).getTuple())
    pygame.display.flip()
