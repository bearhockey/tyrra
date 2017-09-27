import os
import pygame
import random

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
        self.enemies = []
        starting_node = self.find_node("ENTRANCE")
        if starting_node is None:
            starting_point = (3, 3)
        else:
            starting_point = starting_node.tile.x, starting_node.tile.y
            print("STARTING HERE: {0}".format(starting_point))
        self.pc = Entity(name="HERO",
                         image=pygame.image.load(os.path.join(settings.main_path, "res", "digg.png")),
                         x=starting_point[0],
                         y=starting_point[1],
                         portrait=pygame.image.load(os.path.join(settings.main_path, "res/face", "cage.png")))
        # self.entities.append(self.pc)
        self.event_file = os.path.join(settings.main_path, "data", event_file)
        for column in self.grid:
            for node in column:
                if node.node == "SPAWNER" or node.node == "SPAWNER_LIGHT":
                    enemy = Entity(name="CLOONEY{0}".format(random.randint(0, 99)),
                                   image=pygame.image.load(os.path.join(settings.main_path, "res", "george.png")),
                                   y=node.tile.y,
                                   x=node.tile.x,
                                   stats={"HP": 5, "STR": 2, "DEX": 3, "CON": 2, "INT": 1})
                    self.entities.append(enemy)
                    self.enemies.append(enemy)
                    if node.node == "SPAWNER_LIGHT":
                        node.set(node="LIGHT", passable=True)
                    else:
                        node.set()
        # debug
        MapMaker.print_map(self.grid)

    def get_node(self, cord=(0, 0)):
        return self.grid[cord[0]][cord[1]]

    def get_lit_room(self, cord=(0, 0)):
        cord_list = []
        self.recursive_search(cords=cord, node_list=cord_list, search="LIGHT")
        return cord_list

    def recursive_search(self, cords, node_list, search="FLOOR"):
        node = self.get_node(cords)
        if node.node == search and node.tile.get_cords() not in node_list:
            node_list.append(node.tile.get_cords())
            self.recursive_search(cords=node.tile.get_north(), node_list=node_list, search=search)
            self.recursive_search(cords=node.tile.get_south(), node_list=node_list, search=search)
            self.recursive_search(cords=node.tile.get_east(), node_list=node_list, search=search)
            self.recursive_search(cords=node.tile.get_west(), node_list=node_list, search=search)
        else:
            return

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
