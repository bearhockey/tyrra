import pygame
import random

from src.castle.castle_tile import CastleTile as Tile


class CastleEntity(object):
    def __init__(self, image=None, x=0, y=0, tile_size=64, name="ERROR", stats=None, portrait=None):
        self.name = name
        self.image = image
        if image is None:
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((128, 128, 128), pygame.Rect(10, 10, 54, 54))
        self.portrait = portrait
        if portrait is None:
            self.portrait = pygame.Surface((250, 250))
            self.portrait.fill((128, 128, 128), pygame.Rect(10, 10, 230, 230))
        self.tile = Tile(image=self.image, x=x, y=y, tile_size=tile_size)
        self.see()
        self.alive = True
        # stats
        if stats:
            self.stats = stats
        else:
            self.stats = {"HP": 10, "STR": 5, "DEX": 5, "CHR": 5, "CON": 5, "INT": 5, "LCK": 1}
        self.hp = self.stats["HP"]

    def get_position(self):
        return self.tile.get_cords()

    def get_accuracy(self):
        return 1

    def get_soak(self):
        armor = 0 # get armor if you're wearing it
        return armor + self.stats["CON"]

    def direction(self, d):
        if d.lower() == "east":
            return self.tile.get_east()
        elif d.lower() == "west":
            return self.tile.get_west()
        elif d.lower() == "north":
            return self.tile.get_north()
        elif d.lower() == "south":
            return self.tile.get_south()
        else:
            raise Exception("Fuck what direction is this: {0}".format(d))

    def move(self, direction, velocity=1):
        self.tile.move(direction, velocity)

    def teleport(self, position):
        self.tile.move_to(y=position[0], x=position[1])

    def move_towards(self, point):
        self_cords = self.tile.get_cords()
        if self_cords[0] < point[0]:
            y = 1
        elif self_cords[0] > point[0]:
            y = -1
        else:
            y = 0
        if self_cords[1] < point[1]:
            x = 1
        elif self_cords[1] > point[1]:
            x = -1
        else:
            x = 0
        new_position = (self_cords[0]+y, self_cords[1]+x)
        if new_position == point:
            return True
        else:
            self.teleport(position=new_position)
            return False

    def wander(self, parent_map):
        if random.random() > 0.7:
            key, value = random.choice(list(self.tile.compass.items()))
            if parent_map.can_move(self.direction(value)):
                self.move(direction=value)

    def see(self, is_seen=True):
        self.tile.seen = is_seen

    def hurt(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.die()
            return True
        else:
            return False

    def die(self):
        self.see(is_seen=False)
        self.alive = False

    def draw(self, screen, location):
        self.tile.draw(screen, location)
