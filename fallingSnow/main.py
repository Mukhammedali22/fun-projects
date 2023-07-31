import pygame
from random import random, randint
from math import sin, pi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
SCREEN_HIGHT = 720
SCREEN_WIDTH = 1280
BOUNDS = 30
BACKGROUND = "background.png"

running = True
SnowflakeCount = 200

def makeSnow():
    return [Snowflake() for i in range(SnowflakeCount)] 

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
        deltaX = sin(t * 27) + sin(t * 21.3) + 3 * sin(t * 18.75) + 7 * sin(t * 7.6) + 10 * sin(t * 5.23)
        deltaX /= 10
        self.x += deltaX 
        self.y += self.speed
        self.time += self.timeDelta
        if self.y > SCREEN_HIGHT:
            self.makeSnowflake()

    def makeSnowflake(self):
        self.__init__()

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

def set_image(path):
    img =  pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HIGHT))

def main():
    global screen, clock, running
    pygame.init()
    pygame.display.set_caption("fallingSnow")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
    clock = pygame.time.Clock()
    snow = makeSnow()
    background = set_image(BACKGROUND)

    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                running = False
            
        # screen.fill(BLACK)
        screen.blit(background, (0, 0))
        for snowflake in snow:
            snowflake.update()
            snowflake.draw()
        clock.tick(FPS)
        pygame.display.update()

main()