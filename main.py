import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)  # Grass color

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 128, 0)  # Green color for the snake body
        self.head_color = (0, 255, 0)  # Head color

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current_head = self.get_head_position()
        x, y = self.direction
        new_head = (((current_head[0] + (x * GRID_SIZE)) % WIDTH), (current_head[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new_head in self.positions[2:]:
            return False  # Game over
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:
                pygame.draw.rect(surface, self.head_color, (p[0], p[1], GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0, 0, 0), (p[0] + 4, p[1] + 4, GRID_SIZE - 8, GRID_SIZE - 8))


# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GREEN, rect)  # Grass color


def display_score(surface, score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def display_game_over(surface, score):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Your Score: {score}", True, WHITE)

    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.direction = RIGHT

        if not snake.update():
            # Game over
            surface.fill(GREEN)  # Set background color to grass
            draw_grid(surface)
            snake.render(surface)
            food.render(surface)
            display_game_over(surface, score)
            display_score(surface, score)
            screen.blit(surface, (0, 0))
            pygame.display.update()

            pygame.time.wait(2000)  # Wait for 2 seconds
            pygame.quit()
            sys.exit()

        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        surface.fill(GREEN)  # Set background color to grass
        draw_grid(surface)
        snake.render(surface)
        food.render(surface)
        display_score(surface, score)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
