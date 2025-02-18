import pygame
import sys
from time import time, sleep
from random import randint


pygame.init()
clock = pygame.time.Clock()
FPS = 60
def game_loop(window_width: int, window_height: int) -> None:
    field = init_playing_field(window_width, window_height)
    game_over_flag: bool = False
    # timer: float = time()
    score: int = 0
    place_spheres(field, update_preview())
    update_field(field)
    current_preview = update_preview()
    update_hud(score, current_preview)

    while not game_over_flag:
        event = event_manager()
        if event == "mouse_down":
            if reposition_sphere(field):
                place_spheres(field, current_preview)
                current_preview = update_preview()
                update_hud(score, current_preview)
                check_score_con(field)
            
        # test_unit(field)
        clock.tick(FPS)

def check_score_con(field):
    for i in range(len(field)-4):
        for j in range(len(field[i])):
            if not field[i][j][0] == 0:
                current_color = field[i][j][0]
                is_horizontal(field, i, j, current_color, 1)

def is_horizontal(field, i, j, color, amount):
    current_i = i
    current_amount = amount
    field[current_i][j][1] = True
    if not i == len(field)-1:
        if field[current_i+1][j][0] == color:
            field[current_i+1][j][1] = True
            is_horizontal(field, current_i+1, j, color, current_amount+1)
    if i == len(field)-1:
        if current_amount >= 5:
            print(f"{current_amount=}")
            remove_affected(field)
            return [True, current_amount]
        else:
            reset_affected(field)
def remove_affected(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j] = [0, False]
def reset_affected(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j][1] = False
def increase_score(score: int, amount: int) -> int:
    score += amount
    return score

def update_hud(Score, current_preview):
    my_font = pygame.font.SysFont("Arial", 40)
    score = my_font.render(f"{Score=}", True, (255,255,255))
    highscore = my_font.render("0", True, (255,255,255))
    screen.blit(score, (10,0))
    screen.blit(highscore, (10,40))
    for i in range(len(current_preview)):
        match current_preview[i]:
            case 1:
                sphere = pygame.image.load("graphics/sphere_blue_big.png")
            case 2:
                sphere = pygame.image.load("graphics/sphere_red_big.png")
            case 3:
                sphere = pygame.image.load("graphics/sphere_yellow_big.png")
        screen.blit(sphere, ((screen.get_width()//2)-60+40*i, 20))
    pygame.display.update()














# works. do not touch
def place_spheres(field, current_preview):
    for i in range(len(current_preview)):
        invalid_coords = True
        while invalid_coords:
            rand_coords = [randint(0,len(field)-1), randint(0,len(field[0])-1)]
            if field[rand_coords[0]][rand_coords[1]][0] == 0:
                field[rand_coords[0]][rand_coords[1]][0] = current_preview[i]
                invalid_coords = False
    update_field(field)

def update_preview():
    current_preview = [randint(1,3), randint(1,3), randint(1,3)]
    return current_preview

def init_playing_field(width: int, height: int):
    # """ field = [Reihen[Zeilen[Feld[Zustand, betroffen]]]] """
    global screen 
    screen = pygame.display.set_mode([width,height])
    pygame.display.set_caption("Lines98")
    field: list = []
    for i in range(width//40):
        field.append([])
        for _ in range(2, height//40):
            field[i].append([0, False])
    return field

def update_field(field):
    blank_tile = pygame.image.load("graphics/blank.png")
    blue_sphere = pygame.image.load("graphics/sphere_blue_big.png")
    red_sphere = pygame.image.load("graphics/sphere_red_big.png")
    yellow_sphere = pygame.image.load("graphics/sphere_yellow_big.png")
    small_blue_sphere = pygame.image.load("graphics/sphere_blue_small.png")
    small_red_sphere = pygame.image.load("graphics/sphere_red_small.png")
    small_yellow_sphere = pygame.image.load("graphics/sphere_yellow_small.png")
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j][0] == 0:
                screen.blit(blank_tile, (i*40, 80+j*40))
            if field[i][j][0] == 1:
                screen.blit(blue_sphere, (i*40, 80+j*40))
            if field[i][j][0] == 2:
                screen.blit(red_sphere, (i*40, 80+j*40))
            if field[i][j][0] == 3:
                screen.blit(yellow_sphere, (i*40, 80+j*40))
            if field[i][j][0] == 4:
                screen.blit(small_blue_sphere, (i*40, 80+j*40))
            if field[i][j][0] == 5:
                screen.blit(small_red_sphere, (i*40, 80+j*40))
            if field[i][j][0] == 6:
                screen.blit(small_yellow_sphere, (i*40, 80+j*40))
    pygame.display.update()

def event_manager():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                return "mouse_down"
            case pygame.MOUSEBUTTONUP:
                return "mouse_up"

            
def reposition_sphere(field):
    scaled_x = pygame.mouse.get_pos()[0]//40
    scaled_y = (pygame.mouse.get_pos()[1]//40)-2
    sphere = field[scaled_x][scaled_y]
    if mark_sphere(field, sphere):
        select_target(field, sphere)
        return True

def select_target(field, sphere):
    moving_sphere = sphere
    while True:
        event = event_manager()
        target = moving_sphere
        if event == "mouse_down":
            scaled_x = pygame.mouse.get_pos()[0]//40
            scaled_y = (pygame.mouse.get_pos()[1]//40)-2
            target = field[scaled_x][scaled_y]
            if target[0] == 0:
                target[0] = moving_sphere[0]-3
                moving_sphere[0] = 0
                break
            if not target[0] == 0:
                moving_sphere[0] -= 3
                moving_sphere = field[scaled_x][scaled_y]
                moving_sphere[0] += 3
                update_field(field)
    update_field(field)

def mark_sphere(field, sphere):
    if not sphere[0] == 0:
        sphere[0] += 3
        update_field(field)
        return True

def is_key_pressed(key_in_question: int) -> bool:
    keys_pressed = pygame.key.get_pressed()
    return keys_pressed[key_in_question]

def test_unit(field):
    print(pygame.MOUSEBUTTONDOWN)
    if pygame.mouse.get_pressed(3) == (1,0,0):
        print(field[pygame.mouse.get_pos()[0]//40][(pygame.mouse.get_pos()[1]//40)-2][0])

game_loop(800, 480)