import pygame
import random

from Star import Star


class System(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.name = 'Poop'
        self.seed = -self.x * self.y

        self.stars = []
        self.white = (255, 255, 255)

        self.font_size = 24
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)

    def generate_stars(self):
        random.seed(self.seed)
        rand = random.randrange(0, 9)
        self.stars.append(Star(radius=random.randint(1, 255),
                               luminosity=random.randint(1, 255),
                               temperature=random.randint(1, 255)))
        if rand > 6:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))
        if rand > 9:
            self.stars.append(Star(radius=random.randint(1, 255),
                                   luminosity=random.randint(1, 255),
                                   temperature=random.randint(1, 255)))

        sorted(self.stars, key=lambda star: star.radius)

    def draw_stars(self, screen):
        i = 100
        for star in self.stars:
            i += star.radius
            star.draw_grid(screen, (i, 200))
            i += star.radius

    def draw_gui(self, screen):
        pygame.draw.rect(screen, self.white, pygame.Rect(20, 20, 800, 600), 2)
        screen.blit(self.font.render(self.name, True, self.white),
                    pygame.Rect(900, 20, 200, 50))
