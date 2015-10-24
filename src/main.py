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
#system = System(x=531800800, y=867530900)
#system.generate_stars()
planet_map = Map(width/2, height/2, seed=123)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    keys.poll_keyboard(planet_map)

    screen.fill(black)
    # system.draw_stars(screen)
    planet_map.draw(screen)
    # system.draw_gui(screen)

    pygame.display.flip()
