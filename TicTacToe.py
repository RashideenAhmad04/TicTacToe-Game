import pygame
from sys import exit
import os

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 1920, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Up You Go! Xs and Os - Tic Tac Toe")
clock = pygame.time.Clock()

# Loading Screen
Loading_Screen = pygame.image.load("F:\Rashideen\CodingProjects\Rania\Starting_Screen.png").convert()
Loading_Screen = pygame.transform.scale(Loading_Screen, (width, height))
screen.blit(Loading_Screen, (0, 0))

while True:
    # player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Lobby Screen
            Lobby_Screen = pygame.image.load('Lobby.png')
            Lobby_Screen = pygame.transform.scale(Lobby_Screen, (width, height))
            screen.blit(Lobby_Screen, (0, 0))
            pygame.display.flip()
    
    pygame.display.update()
