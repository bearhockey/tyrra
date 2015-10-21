import pygame
import sys

from Controller import Controller
from Map import Map

pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
screen = pygame.display.set_mode(screen_size)

# weird shit get this out of here
avgTemp = 288
tempStep = 0.29

keys = Controller()
planet_map = Map(width/2, height/2)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    keys.poll_keyboard(planet_map)

    screen.fill(black)
    planet_map.draw(screen)

    pygame.display.flip()
