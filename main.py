import pygame
import os
import time
from sys import exit
from random import randint, choices, choice
import math

pygame.init()

#Variables

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Run")
programIcon = pygame.image.load("runner.png")
pygame.display.set_icon(programIcon)
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
font = pygame.font.Font("victor-pixel.ttf", 50)
font2 = pygame.font.Font("victor-pixel.ttf", 100)
font3 = pygame.font.Font("victor-pixel.ttf", 50)
paused_time = 0
obstacle_rect_list = []
player_gravity = 0
jump_speed = -20
fall_speed = 0.8
level = "Easy"
highscore = 0

#Functions
def pause():
    global paused_time, game_active
    paused = True
    pause_start_time = pygame.time.get_ticks()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    paused = False
        screen.blit(play_surf, pause_rect)
        pygame.display.update()
    screen.blit(pause_surf, pause_rect)
    pygame.display.update()
    pause_end_time = pygame.time.get_ticks()
    paused_time += pause_end_time - pause_start_time
    game_active = not paused


def display_score():
    global current_time
    if start_time > 0:
        current_time = pygame.time.get_ticks() - start_time - paused_time
    score_value = int(current_time / 1000) + score_multiplier * 2
    score_surf = font.render("Score: " + f"{score_value}", False, "Black")
    score_rect = score_surf.get_rect(center=(960, 100))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    global speed
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            if obstacle_rect.bottom == 916:
                screen.blit(spider_surf, obstacle_rect)
            else:
                screen.blit(bee_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    global score_multiplier
    if obstacles:
        for i, obstacle_rect in enumerate(obstacles):
            if (
                player.colliderect(obstacle_rect)
                and player.bottom < obstacle_rect.centery
            ):
                obstacles_to_remove.append(i)
                score_multiplier += 1
                screen.blit(enemypoints_surf, enemypoints_rect)
                return True
            if player.colliderect(obstacle_rect) and player.right > obstacle_rect.left:
                return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 916:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def animate_the_run():
    global x_offset
    speed = 0.004
    amplitude = 20
    y_offset = amplitude * math.sin(pygame.time.get_ticks() * speed)
    return y_offset


def animate_start_text():
    global x_offset
    speed = 0.004
    amplitude = 5
    y_offset = amplitude * math.sin(pygame.time.get_ticks() * speed)
    return y_offset


def player_jump():
    global player_gravity
    if player_rect.bottom >= 916:
        player_gravity = -10  # Adjust the jump force to make it higher and floaty


def run_medium():
    global obstacle_rect_list, level
    level = "Medium"
    obstacle_rect_list = []
    pygame.time.set_timer(obstacle_timer, 600)


def run_hard():
    global obstacle_rect_list, level
    level = "Hard"
    obstacle_rect_list = []
    pygame.time.set_timer(obstacle_timer, 200)


def run_easy():
    global obstacle_rect_list, level
    level = "Easy"
    obstacle_rect_list = []
    pygame.time.set_timer(obstacle_timer, 1600)

def spawn_obstacle():
    lane = choice(lanes)
    obstacle_type = choices(obstacle_types, cum_weights=obstacle_spawn_rates, k=1)[0]
    obstacle_width = obstacle_type.get_width()
    obstacle_height = obstacle_type.get_height()
    obstacle_rect = obstacle_type.get_rect(bottomright=(WIDTH, lane))
    obstacle_rect.width = obstacle_width
    obstacle_rect.height = obstacle_height
    max_attempts = 5
    attempts = 0
    while (
        any(obstacle_rect.colliderect(rect) for rect in obstacle_rect_list)
        and attempts < max_attempts
    ):
        lane = choice(lanes)
        obstacle_type = choices(obstacle_types, cum_weights=obstacle_spawn_rates, k=1)[
            0
        ]
        obstacle_width = obstacle_type.get_width()
        obstacle_height = obstacle_type.get_height()
        obstacle_rect = obstacle_type.get_rect(bottomright=(WIDTH, lane))
        obstacle_rect.width = obstacle_width
        obstacle_rect.height = obstacle_height
        attempts += 1
    if attempts < max_attempts:
        return obstacle_rect
    else:
        return None

#Surfaces

sky_surf = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surf = pygame.image.load("graphics/ground2.png").convert_alpha()

    #Player Surfaces

player_walk_1 = pygame.image.load("graphics/player_walk.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player_walk1.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player_jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(bottomleft=(80, 916))

gameover_surf = pygame.image.load("graphics/gameover.png").convert_alpha()

    #Pause Button Surface

pause_surf = pygame.image.load("graphics/pause.png").convert_alpha()
pause_rect = pause_surf.get_rect(center=(50, 50))

    #Play Button Surface

play_surf = pygame.image.load("graphics/play.png").convert_alpha()

    #The Text That Says "The Run"

therun_surf = font2.render("The Run", False, "Black")
therun_rect = therun_surf.get_rect(center=(960, 50))

    #Score Display

score_surf = font.render("Score: ", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

tryagain_surf = font3.render("Press Spacebar To Start, Press Escape To Pause", False, "Black")
tryagain_rect = tryagain_surf.get_rect(center=(960, 1080))

enemypoints_surf = pygame.image.load("graphics/enemypoints.png")
enemypoints_rect = enemypoints_surf.get_rect(topleft=(1100, 110))

    #Obstacle Surfaces [Cactus Not Implemented Yet]

bee_surf = pygame.image.load("graphics/bee.png").convert_alpha()
spider_surf = pygame.image.load("graphics/spider.png").convert_alpha()
cactus_surf = pygame.image.load("graphics/cactus.png")

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)
GROUND_LANE = 916
ABOVE_GROUND_LANE = 826
lanes = [GROUND_LANE, ABOVE_GROUND_LANE]
obstacle_types = [
    bee_surf,
    spider_surf,
]
obstacle_spawn_rates = [0.6, 0.4]


obstacles_to_remove = []
score_multiplier = 0
current_time = 0

while True:
    score_value = int(current_time / 1000) + score_multiplier * 2
    if score_value > highscore:
        highscore = score_value
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 916:
                    player_gravity = jump_speed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    pause()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                score_multiplier = 0
                obstacle_rect_list.clear()

        if event.type == obstacle_timer and game_active:
            obstacle = spawn_obstacle()
            if obstacle:
                obstacle_rect_list.append(obstacle)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 916))

        screen.blit(pause_surf, pause_rect)

        score = display_score()

        #Player
        
        player_gravity += fall_speed
        player_rect.y += player_gravity
        if player_rect.bottom >= 916:
            player_rect.bottom = 916
        player_animation()

        screen.blit(player_surf, player_rect)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect, obstacle_rect_list)
        obstacle_rect_list = [
            obstacle
            for i, obstacle in enumerate(obstacle_rect_list)
            if i not in obstacles_to_remove
        ]
        obstacles_to_remove.clear()
    else:
        screen.blit(gameover_surf, (0, 0))
        screen.blit(therun_surf, therun_rect)
        score_message = font.render(
            "Score: " + f"{(int(current_time / 1000) + score_multiplier * 2)}",
            False,
            "Black",
        )
        score_message_rect = score_message.get_rect(center=(960, 850))
        obstacles_to_remove.clear()

        easy_select = font.render("You Have Selected Easy.", False, "Black")
        easy_select_rect = easy_select.get_rect(topleft=(40, 250))

        medium_select = font.render("You Have Selected Medium.", False, "Black")
        medium_select_rect = medium_select.get_rect(topleft=(40, 250))

        hard_select = font.render("You Have Selected Hard.", False, "Black")
        hard_select_rect = hard_select.get_rect(topleft=(40, 250))

        highscore_surf = font.render("Highscore: " + f"{highscore}", False, "Black")
        highscore_rect = highscore_surf.get_rect(center=(960,770))

        change_difficulty = font.render("Change Difficulty Here:", False, "Black")
        change_difficulty_rect = change_difficulty.get_rect(topleft=(40, 375))

        if level == "Easy":
            screen.blit(easy_select, easy_select_rect)
        elif level == "Medium":
            screen.blit(medium_select, medium_select_rect)
        elif level == "Hard":
            screen.blit(hard_select, hard_select_rect)

        screen.blit(change_difficulty, change_difficulty_rect)

        easy = font.render("Easy", False, "Black")
        easy_rect = easy.get_rect(topleft=(40, 500))
        pygame.draw.rect(screen, "Black", easy_rect, 2)
        screen.blit(easy, easy_rect)

        screen.blit(highscore_surf, highscore_rect)

        medium = font.render("Medium", False, "Black")
        medium_rect = medium.get_rect(topleft=(40, 650))
        pygame.draw.rect(screen, "Black", medium_rect, 2)
        screen.blit(medium, medium_rect)
        hard = font.render("Hard", False, "Black")
        hard_rect = hard.get_rect(topleft=(40, 800))
        pygame.draw.rect(screen, "Black", hard_rect, 2)
        screen.blit(hard, hard_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if medium_rect.collidepoint(event.pos):
                run_medium()
            elif hard_rect.collidepoint(event.pos):
                run_hard()
            elif easy_rect.collidepoint(event.pos):
                run_easy()
        player_rect.midbottom = (80, 916)
        y_offset = animate_the_run()
        therun_rect.y = 50 + y_offset
        screen.blit(therun_surf, therun_rect)
        y_offset = animate_start_text()
        tryagain_rect.y = 950 + y_offset
        screen.blit(tryagain_surf, tryagain_rect)
        paused_time = 0
        if game_active:
            screen.blit(pause_surf, pause_rect)
        else:
            screen.blit(play_surf, pause_rect)
        if score == 0:
            screen.blit(tryagain_surf, tryagain_rect)
        else:
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(120)
