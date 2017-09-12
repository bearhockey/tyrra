import os
import pygame

import settings

from castle.castle_event import CastleEvent as Event
from castle.castle_node import CastleNode as Node
from castle.castle_entity import CastleEntity as Entity
from castle.castle_map_maker import CastleMapMaker as MapMaker


class CastleMap(object):
    def __init__(self, width=10, height=10, tile_size=64, event_file=None):
        self.tile_size = tile_size
        self.size = (height, width)
        # self.grid = MapMaker.make_test_map(width=width, height=height, tile_size=tile_size)
        self.grid = MapMaker.make_dungeon_map(width=width, height=height, tile_size=tile_size, percent_filled=75)
        self.entities = []
        starting_node = self.find_node("ENTRANCE")
        if starting_node is None:
            starting_point = (3, 3)
        else:
            starting_point = starting_node.tile.x, starting_node.tile.y
            print("STARTING HERE: {0}".format(starting_point))
        self.pc = Entity(image=pygame.image.load(os.path.join(settings.main_path, "res", "digg.png")),
                         x=starting_point[0],
                         y=starting_point[1])
        self.entities.append(self.pc)
        self.grid[8][6] = Node(node="EXIT", x=8, y=6, tile_size=self.tile_size, passable=True, event="TEST_1")
        self.event_file = os.path.join(settings.main_path, "data", event_file)
        self.npc = Entity(x=8, y=7)
        self.entities.append(self.npc)
        # debug
        MapMaker.print_map(self.grid)

    def get_node(self, cord=(0, 0)):
        return self.grid[cord[0]][cord[1]]

    def get_event(self, cord=(0, 0)):
        if self.get_node(cord) is not None:
            return self.get_node(cord).event

    def find_node(self, node_type):
        for column in self.grid:
            for node in column:
                if node.node == node_type:
                    return node
        return None

    def can_move(self, cord=(0, 0)):
        if cord[0] < 0 or cord[0] > self.size[0]-1:
            return False
        elif cord[1] < 0 or cord[1] > self.size[1]-1:
            return False
        elif not self.grid[cord[0]][cord[1]].passable:
            return False
        else:
            return True
