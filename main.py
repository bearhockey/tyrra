import pygame
import sys

import settings
import src.const.Color as Color
import src.const.Font as Font
import src.components.Loading as Loading

from src.ControlPanel import ControlPanel
from src.Controller import Controller
from src.CreateCharacter import CreateCharacter
from src.Title import Title

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(settings.screen_size)
Loading.loading_screen(screen)

keys = Controller()
title = Title(font=Font.KAITI_M)
panel = ControlPanel(screen=screen, font=Font.KAITI_M, small_font=Font.KAITI_S)

ship = None
system = None
planet_map = None


mouse_button = {'LEFT': 1, 'MIDDLE': 2, 'RIGHT': 3, 'WHEEL_UP': 4, 'WHEEL_DOWN': 5}

mouse = {mouse_button['LEFT']: 0, mouse_button['MIDDLE']: 0, mouse_button['RIGHT']: 0, mouse_button['WHEEL_UP']: 0,
         mouse_button['WHEEL_DOWN']: 0}

# show fonts for debug purposes
# print pygame.font.get_fonts()

# start game things
# title.play_title_music()
game_mode = "TITLE"

create_character = CreateCharacter(big_font=Font.KAITI_L,
                                   font=Font.KAITI_M,
                                   small_font=Font.KAITI_S,
                                   screen_width=settings.screen_width,
                                   screen_height=settings.screen_height)

while 1:
    clock.tick(60)
    key_pressed = None
    unicode_pressed = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            key_pressed = event.key
            unicode_pressed = event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse[event.button] = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse[event.button] = 0

        if game_mode == "TITLE":
            response = title.update((key_pressed, unicode_pressed), mouse)
            if response == "new":
                game_mode = "NEW"
            elif response == "load":
                title.stop_title_music()
                game_mode = "MAIN"
                panel.new_game()
            elif response == "quit":
                sys.exit(0)
        elif game_mode == "MAIN":
            panel.update((key_pressed, unicode_pressed), mouse)
        elif game_mode == "SHIP":
            ship.update(key_pressed, mouse)
        elif game_mode == "SYSTEM":
            if system:
                system.update((key_pressed, unicode_pressed), mouse)
        elif game_mode == "PLANET":
            if planet_map:
                pass
        elif game_mode == "NEW":
            done = create_character.update((key_pressed, unicode_pressed), mouse)
            if done:
                title.stop_title_music()
                game_mode = "MAIN"
                panel.new_game(captain=done)
    # draw
    screen.fill(Color.BLACK)
    if game_mode == "TITLE" or game_mode == "NEW":
        title.draw(screen)
    elif game_mode == "MAIN":
        # always do always
        panel.always()
        panel.draw(screen)
    elif game_mode == "SHIP":
        ship.draw(screen)
    elif game_mode == "SYSTEM":
        if system:
            system.draw(screen)
    elif game_mode == "PLANET":
        if planet_map:
            planet_map.draw(screen)
    if game_mode == "NEW":
        create_character.draw(screen)

    pygame.display.flip()
