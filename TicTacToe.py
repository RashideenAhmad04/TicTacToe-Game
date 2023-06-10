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
PLAYER_VEL = 7


class Player1(pygame.sprite.Sprite):
    GRAVITY = 1.2

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
        self.turn = True

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
        if self.jump_count == 1:
            self.fall_count = 0

    def check_ready(self):
        self.ready = not self.ready

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.image = pygame.image.load("redplayer.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player2(pygame.sprite.Sprite):
    GRAVITY = 1.2

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
        self.turn = False

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
        if self.jump_count == 1:
            self.fall_count = 0

    def check_ready(self):
        self.ready = not self.ready

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def update(self):
        self.image = pygame.image.load("blueplayer.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        if self.direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(
            join("Images", "Lobby", self.name)).convert_alpha()
        self.width = width
        self.height = height
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)


class platform(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(
            join("Images", "game", self.name)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        screen.blit(self.image, self.rect)


class grid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            join("Images", "game", "white_grid.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.slot = False
        self.chosen = False
        self.state = None

    def update(self):
        if self.slot:
            if self.state == "red":
                self.image = pygame.image.load(
                    join("Images", "game", "1.png")).convert_alpha()
            elif self.state == "blue":
                self.image = pygame.image.load(
                    join("Images", "game", "0.png")).convert_alpha()
        elif self.chosen:
            self.image = pygame.image.load(
                join("Images", "game", "green_grid.png")).convert_alpha()
        else:
            self.image = pygame.image.load(
                join("Images", "game", "white_grid.png")).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
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


def random_platform():
    xcoords = [544, 712, 880, 1048, 1216]
    ycoordsbot = [279, 447, 615, 783, 951]
    ycoordstop = [120, 288, 456, 624,]

    x_values = []
    y_values = []
    for y_value in ycoordsbot:
        x_value = random.choice(xcoords)
        x_value2 = random.choice(xcoords)
        while x_value2 == x_value:
            x_value2 = random.choice(xcoords)
        x_values.append(x_value)
        x_values.append(x_value2)
        y_values.append(y_value)

    for y in ycoordstop:
        x = random.choice(xcoords)
        x_prev = 0
        while x == x_prev:
            x = random.choice(xcoords)
        x_prev = x
        x_values.append(x)
        y_values.append(y)

    platform1 = platform("FLATFORM.png", x_values[0] - 22, y_values[0] - 13)
    platform2 = platform("FLATFORM.png", x_values[1] - 22, y_values[0] - 13)
    platform3 = platform("FLATFORM.png", x_values[2] - 22, y_values[1] - 13)
    platform4 = platform("FLATFORM.png", x_values[3] - 22, y_values[1] - 13)
    platform5 = platform("FLATFORM.png", x_values[4] - 22, y_values[2] - 13)
    platform6 = platform("FLATFORM.png", x_values[5] - 22, y_values[2] - 13)
    platform7 = platform("FLATFORM.png", x_values[6] - 22, y_values[3] - 13)
    platform8 = platform("FLATFORM.png", x_values[7] - 22, y_values[3] - 13)
    platform9 = platform("FLATFORM.png", x_values[8] - 22, y_values[4] - 13)
    platform10 = platform("FLATFORM.png", x_values[9] - 22, y_values[4] - 13)
    platform11 = platform("Vertical_Platforms.png",
                          x_values[10] - 24, y_values[5] - 16)
    platform12 = platform("Vertical_Platforms.png",
                          x_values[11] - 24, y_values[6] - 16)
    platform13 = platform("Vertical_Platforms.png",
                          x_values[12] - 24, y_values[7] - 16)
    platform14 = platform("Vertical_Platforms.png",
                          x_values[13] - 24, y_values[8] - 16)

    game_platforms = [platform1, platform2, platform3, platform4, platform5, platform6,
                      platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14]
    return game_platforms


def grid_init():
    xcoords = [544, 712, 880, 1048, 1216]
    ycoords = [120, 288, 456, 624, 792]
    grids = []

    for x in xcoords:
        for y in ycoords:
            grids.append(grid(x, y))

    return grids


def grid_check(grids, p1, p2):
    i = 0
    
    for grid in grids:
        grid.update()
        if p1.turn:
            if pygame.sprite.collide_mask(p1, grid):
                grids.pop(i)
                for grid2 in grids:
                    grid2.chosen = False
                grid.chosen = True
                grids.insert(i, grid)
            else:
                grid.chosen = False
            i += 1
        elif p2.turn:
            if pygame.sprite.collide_mask(p2, grid):
                grids.pop(i)
                for grid2 in grids:
                    grid2.chosen = False
                grid.chosen = True
                grids.insert(i, grid)
            else:
                grid.chosen = False
            i += 1

def check_winner(grids):
    # Check rows
    for i in range(0, 25, 5):
        if grids[i].state == grids[i + 1].state == grids[i + 2].state == grids[i + 3].state == grids[i + 4].state == "red" or grids[i].state == grids[i + 1].state == grids[i + 2].state == grids[i + 3].state == grids[i + 4].state == "blue":
            return True

    # Check columns
    for i in range(5):
        if grids[i].state == grids[i + 5].state == grids[i + 10].state == grids[i + 15].state == grids[i + 20].state == "red" or grids[i].state == grids[i + 5].state == grids[i + 10].state == grids[i + 15].state == grids[i + 20].state == "blue":
            return True

    # Check diagonals
    if grids[0].state == grids[6].state == grids[12].state == grids[18].state == grids[24].state == "red" or grids[4].state == grids[8].state == grids[12].state == grids[16].state == grids[20].state == "red":
        return True

    if grids[0].state == grids[6].state == grids[12].state == grids[18].state == grids[24].state == "blue" or grids[4].state == grids[8].state == grids[12].state == grids[16].state == grids[20].state == "blue":
        return True
    return False

#def p1_win():
    

def home_screen():
    homescrn = pygame.image.load(
        "Images\Backgrounds\Starting_Screen.png").convert()
    homescrn = pygame.transform.scale(homescrn, (width, height))
    screen.blit(homescrn, (0, 0))
    pygame.display.flip()


def draw_lobby(p1, p2, platforms):
    lobby = pygame.image.load("Images\Backgrounds\lobby1.png").convert()
    lobby = pygame.transform.scale(lobby, (width, height))
    screen.blit(lobby, (0, 0))

    rdy = pygame.image.load(join("Images", "Lobby", "rdy.png")).convert_alpha()
    rdy = pygame.transform.scale(rdy, (216, 40))

    for plat in platforms:
        plat.draw()

    if p1.ready:
        screen.blit(rdy, (176, 136))
    if p2.ready:
        screen.blit(rdy, (1528, 136))

    p1.draw()
    p2.draw()

    pygame.display.flip()


def lobby(p1, p2, objects, platforms, door1, door2):
    p1.rect.x = 456
    p1.rect.y = 832
    p2.rect.x = 1000
    p2.rect.y = 832
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
                if event.key == pygame.K_e and pygame.Rect.colliderect(p1.rect, door1.rect):
                    p1.check_ready()
                if event.key == pygame.K_RCTRL and pygame.Rect.colliderect(p2.rect, door2.rect):
                    p2.check_ready()
        p1.loop(FPS)
        p2.loop(FPS)
        handle_move1(p1, objects)
        handle_move2(p2, objects)
        draw_lobby(p1, p2, platforms)
    pygame.time.wait(500)


def draw_game(p1, p2, platforms, grids):
    game_bg = pygame.image.load("Images\Backgrounds\gamebg.png").convert()
    game_bg = pygame.transform.scale(game_bg, (width, height))
    screen.blit(game_bg, (0, 0))

    for grid in grids:
        grid.draw()

    for platform in platforms:
        platform.draw()

    p1.draw()
    p2.draw()

    pygame.display.update()

def main_game(p1, p2):
    p1.rect.x = 180
    p1.rect.y = 850
    p2.rect.x = 1614
    p2.rect.y = 850
    platforms = random_platform()

    floor_game = pygame.Rect(0, 1048, 1920, 32)
    wall_game = pygame.Rect(31, 0, 1, 1080)
    wall2_game = pygame.Rect(1888, 0, 1, 1080)
    game_objects = [floor_game, wall_game, wall2_game]

    grids = grid_init()

    for platform in platforms:
        game_objects.append(platform.rect)

    game_won = False

    while not game_won:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and p1.jump_count < 2:
                    p1.jump()
                if event.key == pygame.K_UP and p2.jump_count < 2:
                    p2.jump()
                if event.key == pygame.K_e and p1.turn:
                    for grid in grids:
                        if grid.chosen and grid.slot == False:
                            grid.state = "red"
                            grid.slot = True
                            p1.turn = False
                            p2.turn = True
                if event.key == pygame.K_RCTRL:
                    for grid in grids:
                        if grid.chosen and grid.slot == False:
                            grid.state = "blue"
                            grid.slot = True
                            p1.turn = True
                            p2.turn = False

        for grid in grids:
            grid.update()
        p1.loop(FPS)
        p2.loop(FPS)
        handle_move1(p1, game_objects)
        handle_move2(p2, game_objects)
        grid_check(grids, p1, p2)
        draw_game(p1, p2, platforms, grids)
        if check_winner(grids):
            if p1.turn:
                home_screen()
            if p2.turn:
                home_screen()
            game_won = True
            p1.ready = False
            p2.ready = False


def main(screen):
    clock = pygame.time.Clock()
    home_screen()

    p1 = Player1(456, 832, 96, 88)
    p2 = Player2(1000, 832, 96, 88)

    platform1 = object(856, 744, 206, 39, "platform.png")
    platform2 = object(536, 576, 238, 39, "platform.png")
    platform3 = object(1144, 576, 238, 39, "platform.png")
    platform4 = object(88, 392, 391, 39, "platform.png")
    platform5 = object(840, 384, 239, 39, "platform.png")
    platform6 = object(1440, 392, 391, 39, "platform.png")

    floor = pygame.Rect(0, 920, 1920, 160)
    wall = pygame.Rect(24, 0, 1, 1080)
    wall2 = pygame.Rect(1897, 0, 1, 1080)

    door1 = object(88, 199, 391, 231, "reddoor.png")
    door2 = object(1440, 200, 391, 231, "bluedoor.png")

    objects = [floor, wall, wall2, platform1.rect, platform2.rect,
               platform3.rect, platform4.rect, platform5.rect, platform6.rect]
    platforms = [platform1, platform2, platform3,
                 platform4, platform5, platform6, door1, door2]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                lobby(p1, p2, objects, platforms, door1, door2)
                main_game(p1, p2)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(screen)
