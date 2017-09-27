import pygame
import random

import Color
from Controller import Controller

import src.castle.castle_battle as battle
import src.castle.castle_attack_dictionary as atttack_desc
from src.castle.castle_camera import CastleCamera as Camera
from src.castle.castle_event import CastleEvent as Event
from src.castle.castle_map import CastleMap as Map
from src.castle.castle_side import CastleSideBar as Sidebar
from src.components.text.TextBoxList import TextBoxList
from src.components.Window import Window


class Castle(object):
    def __init__(self, tile_size=64, main_window_width=16, main_window_height=8, main_white_space=50,
                 side_window_width=350, side_window_height=650, side_white_space=50, font=None, small_font=None):
        self.tile_size = tile_size
        self.camera = Camera(pos=(main_white_space, main_white_space),
                             size=(main_window_width, main_window_height),
                             tile_size=self.tile_size)
        self.map = Map(width=50, height=30, tile_size=self.tile_size, event_file="test_map.eve")
        # get player for ease
        self.pc = self.map.pc
        self.camera.center_player(self.map.pc.tile.x, self.map.pc.tile.y)
        self.sidebar = Window((main_white_space + main_window_width*tile_size + side_white_space,
                              side_white_space),
                              (side_window_width, side_window_height),
                              name="Sidebar",
                              border_color=Color.d_gray)
        self.sidebar.components.append(Sidebar(player_character=self.pc, font=font, small_font=small_font))

        self.keys = Controller()
        self.console_height = 140
        self.small_font = small_font
        self.console = TextBoxList(pygame.Rect(main_white_space*2,
                                               main_white_space*2+main_window_height*tile_size,
                                               main_window_width*tile_size,
                                               self.console_height),
                                   name='Console', text_color=Color.white, text_outline=True, font=self.small_font,
                                   list_size=5, line_size=20)
        self.console.add_message("TEST MESSAGE")
        self.event = Event(text=self.console)

    def load_event(self, event_file, event_name):
        self.event.read_event_file(event_file)
        self.event.run_event(event_name)

    def add_to_visible(self, node):
        pass

    def see_square(self, cords, visible):
        for y in range(cords[0]-1, cords[0]+2):
            for x in range(cords[1]-1, cords[1]+2):
                if -1 < y < self.map.size[0] and -1 < x < self.map.size[1]:
                    self.map.grid[y][x].see()
                    if (y, x) not in visible:
                        visible.append((y, x))

    def update(self, key, mouse):
        # only do things if tick is true
        tick = False
        pressed = self.keys.poll_keyboard()
        visible_cords = []
        if pressed:
            compass = {"LEFT": "west", "RIGHT": "east", "UP": "north", "DOWN": "south"}
            # seen things
            pc_cords = self.pc.tile.get_cords()
            if self.map.grid[pc_cords[0]][pc_cords[1]].node == "LIGHT":
                room_cords = self.map.get_lit_room(pc_cords)
                for cords in room_cords:
                    self.see_square(cords, visible_cords)
            self.see_square(cords=self.pc.tile.get_cords(), visible=visible_cords)
            for key, value in compass.items():
                if self.keys.check_key(key):
                    tick = True
                    event = self.map.get_event(self.pc.direction(value))
                    engaged_enemy = None
                    for enemy in self.map.enemies:
                        if enemy.tile.get_cords() == self.pc.direction(value):
                            engaged_enemy = enemy
                            break
                    if engaged_enemy:
                        # debug: just kill it and say something
                        damage = battle.melee_attack(attacker=self.pc, defender=engaged_enemy)
                        self.console.add_message(atttack_desc.translate_damage(damage, engaged_enemy.name))
                        if engaged_enemy.hurt(damage=damage):
                            self.map.enemies.remove(engaged_enemy)
                            self.console.add_message("{0} is dead!".format(engaged_enemy.name))
                        # self.console.add_message("KILLED A CLOONEY. {0} left!".format(len(self.map.enemies)))
                    elif event is not None:
                        self.load_event(self.map.event_file, event)
                    elif self.map.can_move(self.pc.direction(value)):
                        self.pc.move(direction=value)
            # enemy shit
            if tick:
                for enemy in self.map.enemies:
                    # is this enemy seen
                    if enemy.tile.get_cords() in visible_cords:
                        enemy.see()
                        if enemy.move_towards(point=self.pc.get_position()):
                            self.console.add_message("{0} attacked you!".format(enemy.name))
                    else:
                        enemy.see(is_seen=False)
                        enemy.wander(self.map)

            self.camera.center_player(player_x=self.map.pc.tile.x, player_y=self.map.pc.tile.y)

    def draw(self, screen):
        self.sidebar.draw(screen)
        self.camera.draw(screen, castle_map=self.map)
        self.console.draw(screen)
