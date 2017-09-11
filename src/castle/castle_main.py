import pygame

import Color
from Controller import Controller

from castle.castle_camera import CastleCamera as Camera
from castle.castle_event import CastleEvent as Event
from castle.castle_map import CastleMap as Map
from components.text.TextBoxList import TextBoxList


class Castle(object):
    def __init__(self, tile_size=64, main_window_width=16, main_window_height=8, main_white_space=50,
                 side_window_width=350, side_window_height=650, side_white_space=50, font=None, small_font=None):
        self.tile_size = tile_size
        self.camera = Camera(pos=(main_white_space, main_white_space),
                             size=(main_window_width, main_window_height),
                             tile_size=self.tile_size)
        self.map = Map(width=32, height=16, tile_size=self.tile_size, event_file="test_map.eve")

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

    def update(self, key, mouse):
        pressed = self.keys.poll_keyboard()
        compass = {"LEFT": "west", "RIGHT": "east", "UP": "north", "DOWN": "south"}
        # seen things
        for y in range(self.map.pc.tile.get_north()[0], self.map.pc.tile.get_south()[0]+1):
            for x in range(self.map.pc.tile.get_west()[1], self.map.pc.tile.get_east()[1]+1):
                if 0 < x < self.map.size[0]-1 and 0 < y < self.map.size[1]-1:
                    self.map.grid[y][x].seen = True
        for key, value in compass.items():
            if self.keys.check_key(key):
                event = self.map.get_event(self.map.pc.direction(value))
                if event is not None:
                    self.load_event(self.map.event_file, event)
                elif self.map.can_move(self.map.pc.direction(value)):
                    self.map.pc.move(direction=value)

        self.camera.center_player(player_x=self.map.pc.tile.x, player_y=self.map.pc.tile.y)

    def draw(self, screen):
        self.camera.draw(screen, castle_map=self.map)
        self.console.draw(screen)
