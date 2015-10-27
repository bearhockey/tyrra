import pygame
import sys

from Controller import Controller
from Map import Map
from Star import Star
from System import System

pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
screen = pygame.display.set_mode(screen_size)

keys = Controller()
system = System(x=2722356, y=11221221)
system.generate_stars()
planet_map = Map(width/2, height/2, seed=123)

mouse_button = {'LEFT': 1, 'MIDDLE': 2, 'RIGHT': 3}

mouse = {mouse_button['LEFT']: 0, mouse_button['MIDDLE']: 0, mouse_button['RIGHT']: 0}

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

    # key_pressed = keys.poll_keyboard()

    screen.fill(black)
    system.draw(screen)
    # planet_map.draw(screen)

    system.update(key_pressed, mouse)

    pygame.display.flip()
