import os
import pygame
import sys

import settings

from src.ControlPanel import ControlPanel
from src.Controller import Controller
from src.CreateCharacter import CreateCharacter
from src.Title import Title
from src.castle.castle_main import Castle


def make_title():
    return Title(font=font, screen_width=width, screen_height=height)


def make_panel():
    return ControlPanel(main_window_width=875,
                        main_window_height=700,
                        main_white_space=10,
                        side_window_width=375,
                        side_window_height=700,
                        side_white_space=10,
                        font=font,
                        small_font=small_font)


def make_castle():
    return Castle(tile_size=64,
                  main_window_width=15,
                  main_window_height=9,
                  main_white_space=10,
                  side_window_width=375,
                  side_window_height=700,
                  side_white_space=10,
                  font=font,
                  small_font=small_font)

settings.init()
pygame.init()
clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
screen = pygame.display.set_mode(screen_size)

huge_font_size = 48
big_font_size = 24
small_font_size = 16
print('heres that file: {0}'.format(os.path.join(settings.main_path, 'res', 'kaiti.ttf')))
big_font = pygame.font.Font(os.path.join(settings.main_path, 'res', 'kaiti.ttf'), huge_font_size)
font = pygame.font.Font(os.path.join(settings.main_path, 'res', 'kaiti.ttf'), big_font_size)
small_font = pygame.font.Font(os.path.join(settings.main_path, 'res', 'kaiti.ttf'), small_font_size)

mode = {"title": 0,
        "main": 1,
        "ship": 2,
        "system": 3,
        "planet": 4,
        "new": 5,
        "castle": 6}

keys = Controller()
title = make_title()
panel = None
ship = None
castle = None
# ship = Ship(size_x=40, size_y=40)
system = None
# system = System()
planet_map = None
# planet_map = Map(width/2, height/2, seed=123)

mouse_button = {"LEFT": 1, "MIDDLE": 2, "RIGHT": 3, "WHEEL_UP": 4, "WHEEL_DOWN": 5}

mouse = {mouse_button["LEFT"]: 0,
         mouse_button["MIDDLE"]: 0,
         mouse_button["RIGHT"]: 0,
         mouse_button["WHEEL_UP"]: 0,
         mouse_button["WHEEL_DOWN"]: 0}

# show fonts for debug purposes
# print pygame.font.get_fonts()

# start game things
# title.play_title_music()
game_mode = mode["title"]

create_character = CreateCharacter(big_font=big_font,
                                   font=font,
                                   small_font=small_font,
                                   screen_width=width,
                                   screen_height=height)

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

        if game_mode == mode['title']:
            response = title.update((key_pressed, unicode_pressed), mouse)
            if response == 'new':
                game_mode = mode['new']
            elif response == 'load':
                title.stop_title_music()
                if castle is None:
                    castle = make_castle()
                game_mode = mode["castle"]
                # if panel is None: panel = make_panel(); panel.new_game()
            elif response == 'quit':
                sys.exit(0)
        elif game_mode == mode['main']:
            if panel is None:
                panel = make_panel()
            panel.update((key_pressed, unicode_pressed), mouse)
        elif game_mode == mode["castle"]:
            if castle is None:
                castle = make_castle()
            castle.update((key_pressed, unicode_pressed), mouse)
        elif game_mode == mode['ship']:
            ship.update(key_pressed, mouse)
        elif game_mode == mode['system']:
            if system:
                system.update((key_pressed, unicode_pressed), mouse)
        elif game_mode == mode['planet']:
            if planet_map:
                pass
        elif game_mode == mode['new']:
            done = create_character.update((key_pressed, unicode_pressed), mouse)
            if done:
                title.stop_title_music()
                game_mode = mode['main']
                if panel is None:
                    panel = make_panel()
                panel.new_game(captain=done)

    key_pressed = keys.poll_keyboard()
    # draw
    screen.fill(black)
    if game_mode == mode["title"] or game_mode == mode["new"]:
        title.draw(screen)
    elif game_mode == mode["main"]:
        # always do always
        panel.always()
        panel.draw(screen)
    elif game_mode == mode["ship"]:
        ship.draw(screen)
    elif game_mode == mode["system"]:
        if system:
            system.draw(screen)
    elif game_mode == mode["planet"]:
        if planet_map:
            planet_map.draw(screen)
    elif game_mode == mode["castle"]:
        castle.draw(screen)
    if game_mode == mode["new"]:
        create_character.draw(screen)

    pygame.display.flip()
