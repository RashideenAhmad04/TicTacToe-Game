import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Up You Go! Xs and Os - Tic Tac Toe")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
grid_size = 5
cell_size = width // grid_size
wall_prob = 0.2

# Player variables
player1_turn = True
player1_symbol = "X"
player2_symbol = "O"

# Create the game grid
grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]

# Create random walls
walls = []
for i in range(grid_size - 1):
    for j in range(grid_size - 1):
        if random.random() < wall_prob:
            walls.append((i, j))

# Main menu loop


def main_menu():
    screen.fill(WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Lobby loop


def lobby():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to be ready", True, BLACK)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    player1_ready = False
    player2_ready = False
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player1_ready and player2_ready:
                        waiting = False
                    elif player1_turn:
                        player1_ready = True
                        player1_turn = False
                    else:
                        player2_ready = True
                        player1_turn = True

# Game loop


def game():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not player1_turn:
                pos = pygame.mouse.get_pos()
                col = pos[0] // cell_size
                row = pos[1] // cell_size
                if grid[row][col] == "":
                    grid[row][col] = player2_symbol
                    player1_turn = True

        # Update screen
        screen.fill(WHITE)

        # Draw grid
        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(j * cell_size, i *
                                   cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLUE, rect, 1)
                if grid[i][j] != "":
                    font = pygame.font.Font(None, 72)
                    text = font.render(grid[i][j], True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)


# Main game loop
while True:
    main_menu()
    lobby()
    game()

# Quit the game
pygame.quit()
