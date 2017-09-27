import pygame

from src.castle.castle_tile import CastleTile as Tile


class CastleNode(object):
    def __init__(self, node="FLOOR", x=0, y=0, image=None, tile_size=64, passable=True, event=None):
        self.tile_size = tile_size
        self.node = node
        self.passable = passable
        if image is None:
            self.image = pygame.Surface((self.tile_size, self.tile_size))
            self.refresh_image()
        else:
            self.image = image

        self.tile = Tile(image=self.image, x=x, y=y, tile_size=tile_size)

        self.event = event

    def see(self, is_seen=True):
        self.tile.seen = is_seen

    def set(self, node="FLOOR", passable=True):
        self.node = node.upper()
        self.passable = passable
        self.refresh_image()

    def refresh_image(self):
        tile_colors = {"WALL": (100, 100, 100, 255),
                       "ENTRANCE": (10, 240, 50, 255),
                       "LIGHT": (200, 200, 250, 255),
                       "EXIT": (0, 50, 250, 255),
                       "DOOR": (250, 250, 25, 255),
                       "FLOOR": (200, 200, 200, 255),
                       "DEAD_END": (230, 230, 230, 255),
                       "SPAWNER": (230, 40, 40, 255),
                       "SPAWNER_LIGHT": (230, 40, 40, 255)}

        self.image.fill(tile_colors[self.node], pygame.Rect(0, 0, self.tile_size, self.tile_size))

    def draw(self, screen, location):
        self.tile.draw(screen, location)
