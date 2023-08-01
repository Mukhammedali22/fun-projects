import pygame
from constants import *
from Snowflake import Snowflake, makeSnow

def main():
    running = True
    pygame.init()
    pygame.display.set_caption("fallingSnow")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
    clock = pygame.time.Clock()
    snow = makeSnow()
    background = pygame.image.load(BACKGROUND).convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HIGHT))
    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.play(-1)

    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                running = False
            
        # screen.fill(BLACK)
        screen.blit(background, (0, 0))
        for snowflake in snow:
            snowflake.update()
            snowflake.draw(screen)
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()
