import pygame as pg
import numpy as np
from time import sleep

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCK_SIZE = 40
BLOCK_NUMBER_X = WINDOW_WIDTH // BLOCK_SIZE
BLOCK_NUMBER_Y = WINDOW_HEIGHT // BLOCK_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GRAY = (169, 169, 169)
GRAY = (128, 128, 128)
LIGHT_SKY_BLUE = (135, 206, 250)
DIGIT_COLOR = (45, 45, 45)
FPS = 30
# 45 75 105 135 165 195 225 255

is_running = True
is_mine = False
game_over = False
you_win = False

images = {
    "1": "images\\Minesweeper_1.png", 
    "2": "images\\Minesweeper_2.png",
    "3": "images\\Minesweeper_3.png",
    "4": "images\\Minesweeper_4.png",
    "5": "images\\Minesweeper_5.png",
    "6": "images\\Minesweeper_6.png",
    "7": "images\\Minesweeper_7.png",
    "8": "images\\Minesweeper_8.png", 
    "flag": "images\\Minesweeper_flag.png",
    "mine": "images\\Minesweeper_mine.png",
    "red_mine": "images\\Minesweeper_red_mine.png",
}

levels = {"easy": 1, "medium": 2, "hard": 3}

class Grid():
    def __init__(self, xlen, ylen) -> None:
        self.grid = np.zeros((xlen, ylen), dtype=int)
        self.used = np.zeros((xlen, ylen), dtype=bool)
        self.red_flag = np.zeros((xlen, ylen), dtype=bool)
        self.xlen = xlen
        self.ylen = ylen
        self.mine_number = 0
        
    def is_safe(self, x: int, y: int) -> bool:
        return 0 <= x < self.xlen and 0 <= y < self.ylen
    
    def set_grid(self, init_i=0, init_j=0, mine=1) -> None:
        self.grid[:, :] = np.random.choice([-1, 0], size=(BLOCK_NUMBER_X, BLOCK_NUMBER_Y), p=[mine/10, (10-mine)/10])
        self.grid[init_i, init_j] = 0
        self.used[:, :] = False
        self.red_flag[:, :] = False
        self.mine_number = np.count_nonzero(self.grid == -1)
                
        for i in range(self.xlen):
            for j in range(self.ylen):
                cnt = 0
                
                if self.is_safe(i, j) and self.grid[i][j] == -1: continue
                if self.is_safe(i - 1, j) and self.grid[i-1][j] == -1: cnt += 1 
                if self.is_safe(i, j - 1) and self.grid[i][j-1] == -1: cnt += 1 
                if self.is_safe(i, j + 1) and self.grid[i][j+1] == -1: cnt += 1 
                if self.is_safe(i + 1, j) and self.grid[i+1][j] == -1: cnt += 1 
                if self.is_safe(i - 1, j - 1) and self.grid[i-1][j-1] == -1: cnt += 1 
                if self.is_safe(i - 1, j + 1) and self.grid[i-1][j+1] == -1: cnt += 1
                if self.is_safe(i + 1, j - 1) and self.grid[i+1][j-1] == -1: cnt += 1 
                if self.is_safe(i + 1, j + 1) and self.grid[i+1][j+1] == -1: cnt += 1
                
                self.grid[i][j] = cnt
                
    def clean_grid(self) -> None:
        self.grid[:, :] = 0
        self.used[:, :] = False
        self.red_flag[:, :] = False
        
    def open_cell(self, i: int, j: int) -> None:
        self.used[i][j] = True
        if 1 <= self.grid[i][j] <= 8:
            return
        
        if self.is_safe(i - 1, j) and not self.used[i-1][j]: self.open_cell(i - 1, j)
        if self.is_safe(i, j - 1) and not self.used[i][j-1]: self.open_cell(i, j - 1)
        if self.is_safe(i, j + 1) and not self.used[i][j+1]: self.open_cell(i, j + 1)
        if self.is_safe(i + 1, j) and not self.used[i+1][j]: self.open_cell(i + 1, j)
        if self.is_safe(i - 1, j - 1) and not self.used[i-1][j-1]: self.open_cell(i - 1, j - 1)
        if self.is_safe(i - 1, j + 1) and not self.used[i-1][j+1]: self.open_cell(i - 1, j + 1)
        if self.is_safe(i + 1, j - 1) and not self.used[i+1][j-1]: self.open_cell(i + 1, j - 1)
        if self.is_safe(i + 1, j + 1) and not self.used[i+1][j+1]: self.open_cell(i + 1, j + 1)   
        
    def is_cleared_grid(self) -> bool:
        remained_cells = np.count_nonzero(self.used == 0)
        flags = np.count_nonzero(self.red_flag == 1)
        return self.mine_number == remained_cells == flags
                             
# pygame 
def draw_grid(obj: Grid):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            i, j = y // BLOCK_SIZE, x // BLOCK_SIZE
            if not obj.used[i][j]:
                if obj.red_flag[i][j]:
                    screen.blit(images.get("flag"), (x, y))
                else: 
                    pg.draw.rect(screen, LIGHT_SKY_BLUE, rect)
            else:  
                if obj.grid[i][j] == -1:
                    screen.blit(images.get("red_mine"), (x, y))
                elif 1 <= obj.grid[i][j] <= 8:
                    screen.blit(images.get(str(obj.grid[i][j])), (x, y))
                else:
                    pg.draw.rect(screen, DARK_GRAY, rect)
            pg.draw.rect(screen, GRAY, rect, 3)

def set_image(path):
    img =  pg.image.load(path).convert_alpha()
    return pg.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))

def draw_instructions():
    restart_button = font_small.render("press \"R\" to restart the game", True, BLACK)
    open_button = font_small.render("press \"O\" to open the grid", True, BLACK)
    close_button = font_small.render("press \"C\" to close the grid", True, BLACK)
    exit_button = font_small.render("press \"X\" to exit the game", True, BLACK)
    easy_button = font_small.render("press \"E\" to play in easy level", True, BLACK)
    medium_button = font_small.render("press \"M\" to play in medium level", True, BLACK)
    hard_button = font_small.render("press \"H\" to play in hard level", True, BLACK)
    screen.blit(easy_button, (40, 170))
    screen.blit(medium_button, (40, 200))
    screen.blit(hard_button, (40, 230))
    screen.blit(restart_button, (40, 260))
    screen.blit(open_button, (40, 290))
    screen.blit(close_button, (40, 320))
    screen.blit(exit_button, (40, 350))

def game_over_screen():
    text = font.render("Game over", True, BLACK)
    screen.fill(RED)
    screen.blit(text, (30, 40))
    draw_instructions()
    
def you_win_screen():
    text = font.render("You win", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (90, 40))
    draw_instructions()

# pygame
def main():
    global screen, clock, is_running, images, G, game_over, you_win, font, font_small
    
    pg.init()
    font = pg.font.SysFont("Verdana", 60)
    font_small = pg.font.SysFont("Verdana", 20)
    screen = pg.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    clock = pg.time.Clock()
    # loading images
    images = dict(map(lambda kv: (kv[0], set_image(kv[1])), images.items()))
    lvl = "easy"
    clicks = 0
    G = Grid(BLOCK_NUMBER_X, BLOCK_NUMBER_Y)
    
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_x):
                is_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                j, i = map(lambda p: p // BLOCK_SIZE, event.pos)
                if event.button == 3: # right click
                    G.red_flag[i][j] = not G.red_flag[i][j]
                elif event.button == 1: # left click
                    clicks += 1
                    if clicks == 1:
                        G.set_grid(init_i=i, init_j=j, mine=levels.get(lvl))
                        print(G.grid)
                        print(G.mine_number)
                        
                    G.used[i][j] = True
                    if G.grid[i][j] == 0:
                        # запускаю рекурсию
                        G.open_cell(i, j)
                    elif G.grid[i][j] == -1:
                        game_over = True
                        draw_grid(obj=G)
                        pg.display.update()
                        sleep(2)
                        game_over_screen()
                        pg.display.update()
                 
                if G.is_cleared_grid():
                    you_win = True
                    G.used.fill(True)
                    draw_grid(obj=G)
                    pg.display.update()
                    sleep(2)
                    you_win_screen()
                    pg.display.update()
                    
            elif event.type == pg.KEYDOWN and event.key == pg.K_e:
                lvl = "easy"
            elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                lvl = "medium"
            elif event.type == pg.KEYDOWN and event.key == pg.K_h:
                lvl = "hard"
            elif event.type == pg.KEYDOWN and event.key == pg.K_o:
                G.used.fill(True)
            elif event.type == pg.KEYDOWN and event.key == pg.K_c:
                G.used.fill(False)
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                G.clean_grid()
                game_over = False
                you_win = False
                clicks = 0
         
        if not game_over and not you_win:
            draw_grid(obj=G)
            pg.display.update()
            clock.tick(FPS)
              
main()
