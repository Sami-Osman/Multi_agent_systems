import random
import pygame

# Constants
NUM_BOMBERMAN = 3
NUM_KILLERMAN = 2
GRID_WIDTH = 20
GRID_HEIGHT = 15
DESTRUCTIBLE_PCT = 30
INDESTRUCTIBLE_PCT = 20
CELL_SIZE = 20  # Size of each cell in pixels

# Image paths
BOMBERMAN_IMAGE_PATH = 'bomberman.png'
KILLERMAN_IMAGE_PATH = 'killer.png'
INDESTRUCTIBLE_WALL_IMAGE_PATH = 'indestructiblewall.png'
DESTRUCTIBLE_WALL_IMAGE_PATH = 'destructiblewall.jpg'
BOMB_IMAGE_PATH = 'bomb.png'

# Function to load and scale images
def load_scaled_image(path):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

# Base agent class
class Agent:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.updated = False  # Flag to check if the agent has been updated in the current loop

    def move(self, direction):
        # Calculate new position based on direction
        new_x, new_y = self.x, self.y
        if direction == 'up':
            new_y -= 1
        elif direction == 'down':
            new_y += 1
        elif direction == 'left':
            new_x -= 1
        elif direction == 'right':
            new_x += 1
        # Check if new position is valid
        if self.grid.is_valid_move(new_x, new_y):
            self.grid.grid[self.y][self.x] = 0  # Clear old position
            self.x, self.y = new_x, new_y
            self.grid.grid[new_y][new_x] = self  
    def update(self):
        # Randomly choose a direction and move
        directions = ['up', 'down', 'left', 'right']
        self.move(random.choice(directions))

# Derived agent classes
class Bomberman(Agent):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)
        self.image = load_scaled_image(BOMBERMAN_IMAGE_PATH)

class Killerman(Agent):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)
        self.image = load_scaled_image(KILLERMAN_IMAGE_PATH)

# Grid class
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['' for _ in range(width)] for _ in range(height)]
        self.init_grid()

    def init_grid(self):
        # Initialize grid with destructible and indestructible walls
        for row in range(self.height):
            for col in range(self.width):
                if (row % 2 == 1) and (col % 2 == 1) and random.randint(0, 100) < INDESTRUCTIBLE_PCT:
                    self.grid[row][col] = 'indestructible'
                elif random.randint(0, 100) < DESTRUCTIBLE_PCT:
                    self.grid[row][col] = 'destructible'

        # Add Bomberman and Killerman agents
        for _ in range(NUM_BOMBERMAN):
            self.add_agent(Bomberman)
        for _ in range(NUM_KILLERMAN):
            self.add_agent(Killerman)
    

    def add_agent(self, agent_class):
        while True:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if self.grid[y][x] == '':
                agent = agent_class(x, y, self)
                self.grid[y][x] = agent
                break

    def is_valid_move(self, x, y):
        # Check if the move is within the grid bounds
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        # Check if the cell is empty
        return self.grid[y][x] == ''

class BombermanGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        pygame.display.set_caption('Bomberman Game')
        self.clock = pygame.time.Clock()
        self.game_grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.destructible_wall_image = load_scaled_image(DESTRUCTIBLE_WALL_IMAGE_PATH)
        self.indestructible_wall_image = load_scaled_image(INDESTRUCTIBLE_WALL_IMAGE_PATH)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update each agent
            for row_index, row in enumerate(self.game_grid.grid):
                for col_index, cell in enumerate(row):
                    if isinstance(cell, Agent) and cell.x == col_index and cell.y == row_index:
                        cell.update()

            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(6)

        pygame.quit()

    def draw_grid(self):
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x, y = col * CELL_SIZE, row * CELL_SIZE
                cell_content = self.game_grid.grid[row][col]
                if isinstance(cell_content, Bomberman):
                    self.screen.blit(cell_content.image, (x, y))
                elif isinstance(cell_content, Killerman):
                    self.screen.blit(cell_content.image, (x, y))
                elif cell_content == 'destructible':
                    self.screen.blit(self.destructible_wall_image, (x, y))
                elif cell_content == 'indestructible':
                    self.screen.blit(self.indestructible_wall_image, (x, y))

def main():
    game = BombermanGame()
    game.run()

if __name__ == "__main__":
    main()
