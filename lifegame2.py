import pygame
from random import randint

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
BLOCK_SIZE = 10
BLOCK_NUMBER_X = WINDOW_WIDTH // BLOCK_SIZE
BLOCK_NUMBER_Y = WINDOW_HEIGHT // BLOCK_SIZE
FPS = 3
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

OLD_GRID = [[False for y in range(BLOCK_NUMBER_Y)] for x in range(BLOCK_NUMBER_X)]
NEW_GRID = [[False for y in range(BLOCK_NUMBER_Y)] for x in range(BLOCK_NUMBER_X)]
FIGURE_GRID = None
IS_RUNNING = True
IN_PAUSE = False
IS_STARTED = False
RANDOM_CONFIG = True

def is_save(x: int, y: int) -> bool:
    return 0 <= x < BLOCK_NUMBER_X and 0 <= y < BLOCK_NUMBER_Y

def random_configuration():
    N = int((BLOCK_NUMBER_X * BLOCK_NUMBER_Y)**0.7)
    for i in range(N):
        x, y = randint(0, BLOCK_NUMBER_X - 1), randint(0, BLOCK_NUMBER_Y - 1)
        OLD_GRID[x][y] = True
        NEW_GRID[x][y] = OLD_GRID[x][y]

def clean_grid():
    for x in range(BLOCK_NUMBER_X):
        for y in range(BLOCK_NUMBER_Y):
            OLD_GRID[x][y] = NEW_GRID[x][y] = False

def check_grid():
    for x in range(BLOCK_NUMBER_X):
        for y in range(BLOCK_NUMBER_Y):
            # NEW_GRID[x][y] = OLD_GRID[x][y]
            cnt = 0
            
            if is_save(x - 1, y) and OLD_GRID[x - 1][y]:
                cnt += 1
            if is_save(x + 1, y) and OLD_GRID[x + 1][y]:
                cnt += 1
            if is_save(x, y - 1) and OLD_GRID[x][y - 1]:
                cnt += 1
            if is_save(x, y + 1) and OLD_GRID[x][y + 1]:
                cnt += 1
            if is_save(x + 1, y + 1) and OLD_GRID[x + 1][y + 1]:
                cnt += 1
            if is_save(x - 1, y + 1) and OLD_GRID[x - 1][y + 1]:
                cnt += 1
            if is_save(x - 1, y - 1) and OLD_GRID[x - 1][y - 1]:
                cnt += 1
            if is_save(x + 1, y - 1) and OLD_GRID[x + 1][y - 1]:
                cnt += 1
            
            if OLD_GRID[x][y]:
                if not 2 <= cnt <= 3:
                    NEW_GRID[x][y] = 0
                    # cell is die
            else:
                if cnt == 3:
                    NEW_GRID[x][y] = 1
                    # cell is born

def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            X, Y = x // BLOCK_SIZE, y // BLOCK_SIZE
            if NEW_GRID[X][Y]:
                pygame.draw.rect(SCREEN, WHITE, rect)
            else:
                pygame.draw.rect(SCREEN, BLACK, rect)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)

    for x in range(BLOCK_NUMBER_X):
        for y in range(BLOCK_NUMBER_Y):
            OLD_GRID[x][y] = NEW_GRID[x][y]
            
def main():
    global SCREEN, CLOCK, IS_RUNNING, IN_PAUSE, IS_STARTED, RANDOM_CONFIG, FIGURE_GRID  
    config = int(input("do you want random configuration?\n1 - yes 0 - no\n"))
    if config:
        RANDOM_CONFIG = True
        random_configuration()  
    else:
        RANDOM_CONFIG = False
    pygame.init()
    pygame.display.set_caption("life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    draw_grid()
    
    while IS_RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                IS_RUNNING = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                X, Y = event.pos[0] // BLOCK_SIZE, event.pos[1] // BLOCK_SIZE
                NEW_GRID[X][Y] = not NEW_GRID[X][Y]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                IS_STARTED = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                IN_PAUSE = not IN_PAUSE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                IS_STARTED = False
                IN_PAUSE = False
                clean_grid()
                if RANDOM_CONFIG:
                    random_configuration()
                draw_grid()
                # print(*NEW_GRID, sep='\n')
                
                
        if IS_STARTED:
            if FIGURE_GRID is None:
                FIGURE_GRID = NEW_GRID 
            if not IN_PAUSE:
                check_grid()
                draw_grid()     
        else:
            if not RANDOM_CONFIG:
                draw_grid()
                # customizing grid
                
        pygame.display.update()
        CLOCK.tick(FPS)  
        
main()
