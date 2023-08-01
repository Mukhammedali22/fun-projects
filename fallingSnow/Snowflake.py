import pygame
from random import random, randint
from constants import *

class Snowflake():
    maxRadius = 4
    maxSpeed = 5
    maxTimeDelta = 0.0015
    def __init__(self):
        self.x = randint(-BOUNDS, SCREEN_WIDTH + BOUNDS)
        self.y = -self.maxRadius
        self.speed = 0.5 + random() * self.maxSpeed
        self.radius = randint(1, self.maxRadius)
        self.time = random() * 2 * pi
        self.timeDelta = random() * self.maxTimeDelta

    def update(self):
        t = self.time
        deltaX = (sin(t * 27) + sin(t * 21.3) + 3 * sin(t * 18.75) 
                  + 7 * sin(t * 7.6) + 10 * sin(t * 5.23))
        deltaX /= 10
        self.x += deltaX 
        self.y += self.speed
        self.time += self.timeDelta
        if self.y > SCREEN_HIGHT:
            self.makeSnowflake()

    def makeSnowflake(self):
        self.__init__()

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
