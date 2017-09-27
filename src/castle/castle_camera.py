import pygame

import src.Color
from src.components.Box import Box


class CastleCamera(object):
    def __init__(self, pos=(0, 0), size=(1, 1), tile_size=64):
        # frame is the viewport where the camera will draw, in a box at the first set of cordinates, with a width
        # and height of the second two cordinates signifiying how many tiles to draw
        adjusted_size = (size[0]*tile_size, size[1]*tile_size)
        self.canvas = pygame.Surface(size=adjusted_size)
        self.position = pos
        self.x_offset = 0
        self.y_offset = 0
        self.frame_size = size
        self.tile_size = tile_size
        self.border = Box(pygame.Rect(pos[0], pos[1], adjusted_size[0], adjusted_size[1]), box_color=None,
                          border_color=src.Color.white, highlight_color=src.Color.white, active_color=src.Color.white)

    def set_offset(self, new_x=0, new_y=0):
        self.x_offset = new_x
        self.y_offset = new_y

    def center_player(self, player_x, player_y):
        # check x
        x_pos = player_x + self.x_offset
        y_pos = player_y + self.y_offset
        if x_pos < int(self.frame_size[0]/3):
            self.x_offset += 1
        elif x_pos > int(self.frame_size[0]*2/3):
            self.x_offset -= 1
        if y_pos < int(self.frame_size[1]/3):
            self.y_offset += 1
        elif y_pos > int(self.frame_size[1]*2/3):
            self.y_offset -= 1

    def get_location(self, tile):
        return (tile.x + self.x_offset)*self.tile_size, (tile.y + self.y_offset)*self.tile_size

    def draw(self, screen, castle_map):
        self.canvas.fill(src.Color.black)
        for row in castle_map.grid:
            for node in row:
                node.draw(self.canvas, self.get_location(node.tile))
        for entity in castle_map.entities:
            entity.draw(self.canvas, self.get_location(entity.tile))
        # always draw player last
        castle_map.pc.draw(self.canvas, self.get_location(castle_map.pc.tile))
        screen.blit(self.canvas, self.position)
        self.border.draw(screen)
