import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

# Set up the game window
width, height = 1920, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Up You Go! Xs and Os - Tic Tac Toe")

FPS = 60
PLAYER_VEL = 5


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def home_screen():
    homescrn = pygame.image.load(
        "Images\Backgrounds\Starting_Screen.png").convert()
    homescrn = pygame.transform.scale(homescrn, (width, height))
    screen.blit(homescrn, (0, 0))
    pygame.display.flip()


def lobby(player):
    Lobby_bg = pygame.image.load("Images\Backgrounds\BG1.png")
    Lobby_bg = pygame.transform.scale(Lobby_bg, (width, height))
    screen.blit(Lobby_bg, (0, 0))

    platform = pygame.image.load(
        "Images\Lobby_Sprites\platform.png").convert_alpha()
    platform = pygame.transform.scale(platform, (208, 40))
    platform_rect = platform.get_rect(center=(960, 705))
    screen.blit(platform, platform_rect)

    player.draw(screen)

    pygame.display.flip()


class Player1(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.sprite = pygame.image.load(
            "Images\Lobby_Sprites\red-among.png").convert_alpha()
        self.sprite = pygame.transfrom.scale(self.sprite, (width, height))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


def handle_move(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)


def main(screen):
    clock = pygame.time.Clock()
    home_screen()

    p1 = Player1(100, 900, 96, 88)
    p1.load_sprite

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                lobby(p1)

    p1.loop(FPS)
    handle_move(p1)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(screen)
