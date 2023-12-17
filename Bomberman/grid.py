import numpy as np
import random
import pygame

# Global variables
GRID_SIZE = 30
INDESTRUCTIBLE_WALL_PERCENTAGE = 10
DESTRUCTIBLE_WALL_PERCENTAGE = 20
NUM_BOMBERAGENTS = 5
NUM_KILLERAGENTS = 2

# Cell types
EMPTY = 0
INDESTRUCTIBLE_WALL = 1
DESTRUCTIBLE_WALL = 2
BAGENT = 3
BOMB = 4
KAGENT = 5
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

# Create a dictionary for image paths
CELL_IMAGES = {
    EMPTY: None,  # You can use None for empty cells
    INDESTRUCTIBLE_WALL: INDESTRUCTIBLE_WALL_IMAGE_PATH,
    DESTRUCTIBLE_WALL: DESTRUCTIBLE_WALL_IMAGE_PATH,
    BAGENT: BOMBERMAN_IMAGE_PATH,
    KAGENT: KILLERMAN_IMAGE_PATH,
    BOMB: BOMB_IMAGE_PATH,
}


# Initialize Pygame
pygame.init()

# Set up display
CELL_SIZE = 20
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman RL")

# BOMBER Agent Class
class BAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def move(self, direction, grid):
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

        # Check if new position is within grid bounds and either empty or a bomb
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if grid[new_x][new_y] in [EMPTY, BOMB]:
                grid[self.x][self.y] = EMPTY
                self.x, self.y = new_x, new_y

    def make_decision(self, grid, bombs):
        if random.random() < 0.2:  # 20% chance to plant a bomb
            self.plant_bomb(bombs, grid)
        else:
            directions = ['up', 'down', 'left', 'right']
            self.move(random.choice(directions), grid)

    def plant_bomb(self, bombs, grid):
        if grid[self.x][self.y] == EMPTY:
            bomb = Bomb(self.x, self.y)
            bombs.append(bomb)
            grid[self.x][self.y] = BOMB
    def check_collision_with_killerman(self, killermen):
        for killerman in killermen:
            if killerman.alive and self.x == killerman.x and self.y == killerman.y:
                self.alive = False
# Killerman Class
class Killerman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def move(self, grid):
        # Calculate random movement
        directions = ['up', 'down', 'left', 'right']
        random_direction = random.choice(directions)
        new_x, new_y = self.x, self.y

        if random_direction == 'up':
            new_y -= 1
        elif random_direction == 'down':
            new_y += 1
        elif random_direction == 'left':
            new_x -= 1
        elif random_direction == 'right':
            new_x += 1

        # Check if new position is within grid bounds and either empty or a bomb
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if grid[new_x][new_y] in [EMPTY, BOMB, BAGENT]:
                grid[self.x][self.y] = EMPTY
                self.x, self.y = new_x, new_y

# Bomb Class
class Bomb:
    def __init__(self, x, y, countdown=15, radius=1):
        self.x = x
        self.y = y
        self.countdown = countdown
        self.radius = radius

    def tick(self):
        self.countdown -= 1

    def has_exploded(self):
        return self.countdown <= 0

    def explode(self, grid, bagents, kagents):
        # Affect the center cell
        if grid[self.x][self.y] == BOMB:
            grid[self.x][self.y] = EMPTY


        # Affect surrounding cells
        for dx in range(-self.radius, self.radius + 1):
            for dy in range(-self.radius, self.radius + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[nx][ny] == DESTRUCTIBLE_WALL:
                        grid[nx][ny] = EMPTY
                    elif grid[nx][ny] == BAGENT:
                        for agent in bagents:
                            if agent.x == nx and agent.y == ny:
                                agent.alive = False
                    elif grid[nx][ny] == KAGENT:
                        for agent in kagents:
                            if agent.x == nx and agent.y == ny:
                                agent.alive = False
        for agent in bagents:
            if self.x - self.radius <= agent.x <= self.x + self.radius and \
               self.y - self.radius <= agent.y <= self.y + self.radius:
                agent.alive = False
        for agent in kagents:
            if self.x - self.radius <= agent.x <= self.x + self.radius and \
               self.y - self.radius <= agent.y <= self.y + self.radius:
                agent.alive = False

def initialize_grid():
    grid = np.full((GRID_SIZE, GRID_SIZE), EMPTY)

    # Add indestructible walls
    num_indestructible_walls = int(GRID_SIZE * GRID_SIZE * INDESTRUCTIBLE_WALL_PERCENTAGE / 100)
    while num_indestructible_walls > 0:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = INDESTRUCTIBLE_WALL
            num_indestructible_walls -= 1

    # Add destructible walls
    num_destructible_walls = int(GRID_SIZE * GRID_SIZE * DESTRUCTIBLE_WALL_PERCENTAGE / 100)
    while num_destructible_walls > 0:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = DESTRUCTIBLE_WALL
            num_destructible_walls -= 1
    
    bombers = []
    for _ in range(NUM_BOMBERAGENTS):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[x][y] == EMPTY:
                agent = BAgent(x, y)
                bombers.append(agent)
                grid[x][y] = BAGENT
                break

    # Initialize Killerman agents
    killers = []
    for _ in range(NUM_KILLERAGENTS):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[x][y] == EMPTY:
                agent = Killerman(x, y)
                killers.append(agent)
                grid[x][y] = KAGENT
                break

    return grid, bombers, killers


# Modify the draw_grid function
def draw_grid(grid, bagents, kagents, bombs, screen):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_type = grid[x][y]
            image_path = CELL_IMAGES[cell_type]

            if image_path is not None:
                image = load_scaled_image(image_path)
                screen.blit(image, rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect)

    for agent in bagents:
        if agent.alive:
            agent_rect = pygame.Rect(agent.x * CELL_SIZE, agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            image = load_scaled_image(CELL_IMAGES[BAGENT])
            screen.blit(image, agent_rect)
    for agent in kagents:
        if agent.alive:
            agent_rect = pygame.Rect(agent.x * CELL_SIZE, agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            image = load_scaled_image(CELL_IMAGES[KAGENT])
            screen.blit(image, agent_rect)
    for bomb in bombs:
        bomb_rect = pygame.Rect(bomb.x * CELL_SIZE, bomb.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        image = load_scaled_image(CELL_IMAGES[BOMB])
        screen.blit(image, bomb_rect)


def main():
    grid, bombers, killers = initialize_grid()
    bombs = []
    running = True
    clock = pygame.time.Clock()

    # Initial drawing of the grid
    screen.fill((0, 0, 0))
    draw_grid(grid, bombers, killers, bombs, screen)  # Combine bombers and killermen in the agents list
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bomb in bombs[:]:
            bomb.tick()
            if bomb.has_exploded():
                bomb.explode(grid, bombers, killers)
                bombs.remove(bomb)

        for agent in bombers:
            if agent.alive:
                agent.make_decision(grid, bombs)

        for killerman in killers:
            if killerman.alive:
                killerman.move(grid)  # Move the Killerman agents

        # Check collisions for Bomberman and Killerman
        for bomber in bombers:
            if bomber.alive:
                bomber.check_collision_with_killerman(killers)

        screen.fill((0, 0, 0))
        draw_grid(grid, bombers, killers, bombs, screen)  # Combine bombers and killermen in the agents list
        pygame.display.flip()
        clock.tick(5)  # Adjust the frame rate as needed

    pygame.quit()

if __name__ == "__main__":
    main()
