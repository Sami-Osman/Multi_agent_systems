import random

# Constants
GRID_SIZE = 25
DESTRUCTIBLE_WALL_PERCENTAGE = 0.3
INDESTRUCTIBLE_WALL_PERCENTAGE = 0.2

# Cell types
OPEN_SPACE = ' '
DESTRUCTIBLE_WALL = 'D'
INDESTRUCTIBLE_WALL = 'I'
BOMBERMAN = 'B'
KILLERMAN = 'K'
BOMB = 'X'

# Directions
DIRECTIONS = ['up', 'down', 'left', 'right']

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[OPEN_SPACE for _ in range(size)] for _ in range(size)]
        self.place_walls()

    def place_walls(self):
        # Place indestructible walls
        for i in range(0, self.size, 2):
            for j in range(0, self.size, 2):
                self.grid[i][j] = INDESTRUCTIBLE_WALL

        # Place destructible walls
        destructible_wall_count = int(self.size ** 2 * DESTRUCTIBLE_WALL_PERCENTAGE)
        while destructible_wall_count > 0:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[x][y] == OPEN_SPACE:
                self.grid[x][y] = DESTRUCTIBLE_WALL
                destructible_wall_count -= 1

    def display(self):
        for row in self.grid:
            print(' '.join(row))

class Agent:
    def __init__(self, grid, symbol):
        self.grid = grid
        self.symbol = symbol
        self.place_agent()

    def place_agent(self):
        while True:
            x, y = random.randint(0, self.grid.size-1), random.randint(0, self.grid.size-1)
            if self.grid.grid[x][y] == OPEN_SPACE:
                self.grid.grid[x][y] = self.symbol
                self.x, self.y = x, y
                break

    def move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == 'up':
            new_x -= 1
        elif direction == 'down':
            new_x += 1
        elif direction == 'left':
            new_y -= 1
        elif direction == 'right':
            new_y += 1

        if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size and \
           self.grid.grid[new_x][new_y] in [OPEN_SPACE, DESTRUCTIBLE_WALL]:
            self.grid.grid[self.x][self.y] = OPEN_SPACE
            self.x, self.y = new_x, new_y
            self.grid.grid[new_x][new_y] = self.symbol

class Bomberman(Agent):
    def __init__(self, grid):
        super().__init__(grid, BOMBERMAN)

class Killerman(Agent):
    def __init__(self, grid):
        super().__init__(grid, KILLERMAN)

class Bomb:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y
        self.timer = 3  # seconds
        self.grid.grid[x][y] = BOMB

    def explode(self):
        # Explode and affect adjacent cells
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.grid.size and 0 <= ny < self.grid.size:
                if self.grid.grid[nx][ny] == DESTRUCTIBLE_WALL:
                    self.grid.grid[nx][ny] = OPEN_SPACE

        # Clear the bomb
        self.grid.grid[self.x][self.y] = OPEN_SPACE

# Main game loop (simplified)
def main():
    grid = Grid(GRID_SIZE)
    bomberman = Bomberman(grid)
    killerman = Killerman(grid)

    # Example moves and bomb placement
    bomberman.move('up')
    bomb = Bomb(grid, bomberman.x, bomberman.y)
    grid.display()
    bomb.explode()
    grid.display()

if __name__ == "__main__":
    main()
