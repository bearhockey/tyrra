import pygame
import sys

from Controller import Controller
from Map import Map
from Ship import Ship
from System import System

pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
screen = pygame.display.set_mode(screen_size)

mode = {'ship': 0,
        'system': 1,
        'planet': 2}

game_mode = mode['ship']
keys = Controller()
ship = Ship(size_x=40, size_y=40)
# system = None
system = System()
planet_map = None
# planet_map = Map(width/2, height/2, seed=123)

mouse_button = {'LEFT': 1, 'MIDDLE': 2, 'RIGHT': 3, 'WHEEL_UP': 4, 'WHEEL_DOWN': 5}

mouse = {mouse_button['LEFT']: 0, mouse_button['MIDDLE']: 0, mouse_button['RIGHT']: 0, mouse_button['WHEEL_UP']: 0,
         mouse_button['WHEEL_DOWN']: 0}

# show fonts for debug purposes
print pygame.font.get_fonts()

while 1:
    clock.tick(60)
    key_pressed = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            key_pressed = event.key
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse[event.button] = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse[event.button] = 0

        if game_mode == mode['ship']:
            ship.update(key_pressed, mouse)
        elif game_mode == mode['system']:
            if system:
                system.update(key_pressed, mouse)
        elif game_mode == mode['planet']:
            if planet_map:
                pass

    # key_pressed = keys.poll_keyboard()

    screen.fill(black)
    if game_mode == mode['ship']:
        ship.draw(screen)
    elif game_mode == mode['system']:
        if system:
            system.draw(screen)
    elif game_mode == mode['planet']:
        if planet_map:
            planet_map.draw(screen)

    pygame.display.flip()
