import pygame
import random


class CastleTile(object):
    def __init__(self, image=None, x=0, y=0, tile_size=64):
        self.tile_size = tile_size
        self.x = x
        self.y = y
        self.image = image
        if image is None:
            self.image = pygame.Surface((self.tile_size, self.tile_size))
            self.image.fill((128, 128, 128), pygame.Rect(10, 10, 54, 54))
        self.seen = False
        self.compass = {"LEFT": "west", "RIGHT": "east", "UP": "north", "DOWN": "south"}

    def get_cords(self):
        return self.y, self.x

    def get_east(self):
        return self.y, self.x+1

    def get_west(self):
        return self.y, self.x-1

    def get_north(self):
        return self.y-1, self.x

    def get_south(self):
        return self.y+1, self.x

    def move_to(self, y=0, x=0):
        self.x = x
        self.y = y

    def move(self, direction=None, velocity=1):
        # 0,0 is top left corner
        if direction.lower() == "north":
            self.y -= velocity
        elif direction.lower() == "south":
            self.y += velocity
        elif direction.lower() == "east":
            self.x += velocity
        elif direction.lower() == "west":
            self.x -= velocity
        else:
            print("Invalid direction given; not moving tile")

    def move_random(self, velocity=1):
        self.move(direction=random.choice(["north", "south", "east", "west"], velocity=velocity))

    def draw(self, screen, location):
        if self.seen:
            screen.blit(self.image, dest=location)
