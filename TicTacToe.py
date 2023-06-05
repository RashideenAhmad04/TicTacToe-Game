import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
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

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.sprite = pygame.image.load("redplayer.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
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
        


    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.sprite = pygame.image.load("blueplayer.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
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
        self.image = pygame.image.load("Images\Lobby_Sprites\platform.png").convert_alpha()
        self.width = width
        self.height = height

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)

def vertical_collision1(p1, objects, dy1):
    for obj in objects:
        if pygame.Rect.colliderect(p1.rect, obj.rect):
            if dy1 > 0:
                p1.rect.bottom = obj.rect.top
                p1.landed()
            elif dy1 < 0:
                p1.rect.top = obj.rect.bottom
                p1.hit_head()

def vertical_collision2(p2, objects, dy2 ):
    for obj in objects:
        if pygame.Rect.colliderect(p2.rect, obj.rect):
            if dy2 > 0:
                p2.rect.bottom = obj.rect.top
                p2.landed()
            elif dy2 < 0:
                p2.rect.top = obj.rect.bottom
                p2.hit_head()

def collide1(p1, objects, dx1):
    p1.move(dx1, 0)
    p1.update()
    collided_object = None
    for obj in objects:
        if pygame.Rect.colliderect(p1.rect, obj.rect):
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
        if pygame.Rect.colliderect(p2.rect, obj.rect):
            collided_object = obj
            break

    p2.move(-dx2, 0)
    p2.update()
    return collided_object

def ground_collision1(p1, dy1):
    ground_rect = pygame.Rect(0, 920, 1920, 160)
    if pygame.Rect.colliderect(p1.rect, ground_rect):
            if dy1 > 0:
                p1.rect.bottom = ground_rect.top
                p1.landed()

def ground_collision2(p2, dy2):
    ground_rect = pygame.Rect(0, 920, 1920, 160)
    if pygame.Rect.colliderect(p2.rect, ground_rect):
            if dy2 > 0:
                p2.rect.bottom = ground_rect.top
                p2.landed()
            elif dy2 < 0:
                p2.rect.top = ground_rect.bottom
                p2.hit_head()

def handle_move1(p1, objects):

    keys = pygame.key.get_pressed()

    p1.x_vel = 0
    collide_left = collide1(p1, objects, -PLAYER_VEL * 2)
    collide_right = collide1(p1, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        p1.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        p1.move_right(PLAYER_VEL)

    ground_collision1(p1, p1.y_vel)
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

    ground_collision2(p2, p2.y_vel)
    vertical_collision1(p2, objects, p2.y_vel)

def home_screen():
    homescrn = pygame.image.load("Images\Backgrounds\Starting_Screen.png").convert()
    homescrn = pygame.transform.scale(homescrn, (width, height))
    screen.blit(homescrn, (0, 0))
    pygame.display.flip()

def draw_lobby(p1, p2, objects):
    lobby = pygame.image.load("Images\Backgrounds\BG1.png").convert()
    lobby = pygame.transform.scale(lobby, (width, height))
    screen.blit(lobby, (0, 0))

    p1.draw()
    p2.draw()

    for obj in objects:
        obj.draw()

    pygame.display.flip()

def lobby(p1, p2, objects):
    while not(p1.ready) and not(p2.ready):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and p1.jump_count < 2:
                    p1.jump()
                if event.key == pygame.K_UP and p2.jump_count < 2:
                    p2.jump()

        p1.loop(FPS)
        p2.loop(FPS)
        handle_move1(p1, objects)
        handle_move2(p2, objects)
        draw_lobby(p1, p2, objects)


def main(screen):
    clock = pygame.time.Clock()
    home_screen()
    

    p1 = Player1(456, 832, 96,88)
    p2 = Player2(1000, 832, 96,88)

    platform1 = platform(856, 744 , 206, 38)
    platform2 = platform(536, 576 , 238, 38)
    platform3 = platform(1144, 576 , 238, 38)

    objects = [platform1, platform2, platform3]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                lobby(p1, p2, objects)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(screen)