import numpy as np

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
        self.grid[:, :] = np.random.choice([-1, 0], size=(self.xlen, self.ylen), p=[mine/10, (10-mine)/10])
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
 