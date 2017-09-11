import pygame

from src.castle.castle_tile import CastleTile as Tile


class CastleEntity(object):
    def __init__(self, image=None, x=0, y=0, tile_size=64):
        self.image = image
        if image is None:
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((128, 128, 128), pygame.Rect(10, 10, 54, 54))
        self.tile = Tile(image=self.image, x=x, y=y, tile_size=tile_size)

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

    def draw(self, screen, location):
        self.tile.draw(screen, location)
