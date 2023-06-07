from os.path import isfile, join
from os import listdir
import pygame
import math
import random
import os
pygame.init()

# Set up the game window
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Up You Go! Xs and Os - Tic Tac Toe")

FPS = 60
PLAYER_VEL = 5


class Player1(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.ready = False
        self.fall_count = 0
        self.jump_count = 0
        self.width = width
        self.height = height

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

    def jump(self):
        self.y_vel = -self.GRAVITY * 10
        self.jump_count += 1

    def check_ready(self):
        self.ready = not self.ready

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.sprite = pygame.image.load("redplayer.png").convert_alpha()
        self.sprite = pygame.transform.scale(
            self.sprite, (self.width, self.height))
        if self.direction == "left":
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Player2(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.ready = False
        self.fall_count = 0
        self.jump_count = 0
        self.width = width
        self.height = height

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

    def jump(self):
        self.y_vel = -self.GRAVITY * 10
        self.jump_count += 1

    def check_ready(self):
        self.ready = not self.ready

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.sprite = pygame.image.load("blueplayer.png").convert_alpha()
        self.sprite = pygame.transform.scale(
            self.sprite, (self.width, self.height))
        if self.direction == "right":
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("Images\Lobby\platform.png").convert_alpha()
        self.width = width
        self.height = height

    def draw(self):
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)

class door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(join("Images", "Lobby", self.name)).convert_alpha()
        self.width = width
        self.height = height
    def draw(self):
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)
    

def vertical_collision1(p1, objects, dy1):
    for obj in objects:
        if pygame.Rect.colliderect(p1.rect, obj):
            if dy1 > 0:
                p1.rect.bottom = obj.top
                p1.landed()
            elif dy1 < 0:
                p1.rect.top = obj.bottom
                p1.hit_head()


def vertical_collision2(p2, objects, dy2):
    for obj in objects:
        if pygame.Rect.colliderect(p2.rect, obj):
            if dy2 > 0:
                p2.rect.bottom = obj.top
                p2.landed()
            elif dy2 < 0:
                p2.rect.top = obj.bottom
                p2.hit_head()


def collide1(p1, objects, dx1):
    p1.move(dx1, 0)
    p1.update()
    collided_object = None
    for obj in objects:
        if pygame.Rect.colliderect(p1.rect, obj):
            collided_object = obj
            break

    p1.move(-dx1, 0)
    p1.update()
    return collided_object


def collide2(p2, objects, dx2):
    p2.move(dx2, 0)
    p2.update()
    collided_object = None
    for obj in objects:
        if pygame.Rect.colliderect(p2.rect, obj):
            collided_object = obj
            break

    p2.move(-dx2, 0)
    p2.update()
    return collided_object

def handle_move1(p1, objects):

    keys = pygame.key.get_pressed()

    p1.x_vel = 0
    collide_left = collide1(p1, objects, -PLAYER_VEL * 2)
    collide_right = collide1(p1, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        p1.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        p1.move_right(PLAYER_VEL)

    vertical_collision1(p1, objects, p1.y_vel)


def handle_move2(p2, objects):
    keys = pygame.key.get_pressed()

    p2.x_vel = 0
    collide_left = collide1(p2, objects, -PLAYER_VEL * 2)
    collide_right = collide1(p2, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        p2.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        p2.move_right(PLAYER_VEL)

    vertical_collision1(p2, objects, p2.y_vel)


def home_screen():
    homescrn = pygame.image.load(
        "Images\Backgrounds\Starting_Screen.png").convert()
    homescrn = pygame.transform.scale(homescrn, (width, height))
    screen.blit(homescrn, (0, 0))
    pygame.display.flip()


def draw_lobby(p1, p2, platforms):
    lobby = pygame.image.load("Images\Backgrounds\BG1.png").convert()
    lobby = pygame.transform.scale(lobby, (width, height))
    screen.blit(lobby, (0, 0))

    for plat in platforms:
        plat.draw()

    p1.draw()
    p2.draw()

    pygame.display.flip()


def lobby(p1, p2, objects, platforms, door1, door2):
    while not (p1.ready) or not (p2.ready):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and p1.jump_count < 1:
                    p1.jump()
                if event.key == pygame.K_UP and p2.jump_count < 1:
                    p2.jump()
                if event.key == pygame.K_e and pygame.Rect.colliderect(p1.rect,door1.rect):
                    p1.check_ready()
                if event.key == pygame.K_RCTRL and pygame.Rect.colliderect(p2.rect,door2.rect):
                    p2.check_ready()
        p1.loop(FPS)
        p2.loop(FPS)
        handle_move1(p1, objects)
        handle_move2(p2, objects)
        draw_lobby(p1, p2, platforms)

def main_game():
    game_bg = pygame.image.load("Images\Backgrounds\game.png").convert()
    game_bg = pygame.transform.scale(game_bg, (width, height))
    screen.blit(game_bg, (0, 0))
    pygame.display.update()



def main(screen):
    clock = pygame.time.Clock()
    home_screen()

    p1 = Player1(456, 832, 96, 88)
    p2 = Player2(1000, 832, 96, 88)

    platform1 = platform(856, 744, 206, 39)
    platform2 = platform(536, 576, 238, 39)
    platform3 = platform(1144, 576, 238, 39)
    platform4 = platform(88, 392, 391, 39)
    platform5 = platform(840, 384, 239, 39)
    platform6 = platform(1440, 392, 391, 39)

    floor = pygame.Rect(0, 920, 1920, 160)
    wall = pygame.Rect(24, 0, 1, 1080)
    wall2 = pygame.Rect(1897, 0, 1, 1080)

    door1 = door(88, 199, 391, 231, "reddoor.png")
    door2 = door(1440, 200,391, 231, "bluedoor.png")

    objects = [ floor, wall, wall2, platform1.rect, platform2.rect, platform3.rect, platform4.rect, platform5.rect, platform6.rect]
    platforms = [platform1, platform2, platform3, platform4, platform5, platform6, door1, door2]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                lobby(p1, p2, objects, platforms, door1, door2)
                main_game()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(screen)
