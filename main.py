import pygame
from random import randint as rn
import math

pygame.init()

screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)


pause_img = pygame.image.load('images/pause.jpg')
pre_pro_background = pygame.image.load('images/background0.jpg')
background = pygame.transform.scale(pre_pro_background, screen_size)

clock = pygame.time.Clock()
running = True
dt = 0


number_of_rain_drops = 5000
rain_obj_pos = [[rn(0, screen_size[0]), rn(0, screen_size[1])] for _ in range(number_of_rain_drops)]
rain_radius = [rn(1, 3) for _ in range(number_of_rain_drops)]
rain_color = "darkblue"
rain_speed = 10

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_radius = 40
player_speed = 200
player_color = "black"


def cir_col(circle1xy, circle2xy, circle1_radius, circle2_radius):
    dx = circle2xy[0] - circle1xy[0]
    dy = circle2xy[1] - circle1xy[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Check for collision
    if distance <= circle1_radius + circle2_radius:
        return True


def center_detect(cir1xy, cir2xy):
    if cir1xy[0] > cir2xy[0]:
        return True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, player_color, player_pos, player_radius)

    for x in range(len(rain_obj_pos)):
        pygame.draw.circle(screen, rain_color, rain_obj_pos[x], rain_radius[x])
        rain_obj_pos[x][1] += rn(1, 10)
        if rain_obj_pos[x][1] > screen_size[1]:
            rain_obj_pos[x][1] = 0
            rain_obj_pos[x][0] = rn(0, screen_size[0])

        if cir_col(rain_obj_pos[x], player_pos, rain_radius[x], player_radius):
            if center_detect(rain_obj_pos[x], player_pos):
                rain_obj_pos[x][0] += 25
            else:
                rain_obj_pos[x][0] -= 25
            rain_obj_pos[x][1] -= rain_speed

    if player_pos[0] > screen_size[0]:
        player_pos[0] = 0
    if player_pos[0] < 0:
        player_pos[0] = screen_size[0]
    if player_pos[1] > screen_size[1]:
        player_pos[1] = 0
    if player_pos[1] < 0:
        player_pos[1] = screen_size[1]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        player_pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player_pos.x += player_speed * dt
    if keys[pygame.K_p]:
        pygame.time.wait(8)
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys2 = pygame.key.get_pressed()
            screen.blit(pause_img, (0, 0))
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            if keys2[pygame.K_p]:
                paused = False
            if keys2[pygame.K_ESCAPE]:
                running = False
                paused = False
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_F11]:
        is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
        if is_fullscreen:
            screen = pygame.display.set_mode(screen_size)
            pygame.time.wait(10)
        else:
            screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
            pygame.time.wait(10)


    pygame.display.flip()

    dt = clock.tick(60) / 1000
