import pygame
import random

from InputBox import InputBox
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

        # input boxes
        self.x_box = InputBox(pygame.Rect(100, 650, 200, 50), (10, 10, 10), self.white, '0', self.white, self.font)
        self.y_box = InputBox(pygame.Rect(400, 650, 200, 50), (10, 10, 10), self.white, '0', self.white, self.font)

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

    def draw_text(self, screen, text, color, position):
        screen.blit(self.font.render(text, True, color), pygame.Rect(position[0], position[1], 200, 50))

    def draw_stars(self, screen):
        i = 100
        for star in self.stars:
            i += star.radius
            star.draw_grid(screen, (i, 200))
            i += star.radius

    def draw_gui(self, screen):
        pygame.draw.rect(screen, self.white, pygame.Rect(20, 20, 800, 600), 2)
        # cords
        self.draw_text(screen, 'X:', self.white, (900, 650))
        self.draw_text(screen, 'Y:', self.white, (980, 650))
        self.x_box.draw(screen)
        self.y_box.draw(screen)
        self.draw_text(screen, self.name, self.white, (900, 20))
        self.draw_text(screen, 'Suns: {0}'.format(len(self.stars)), self.white, (900, 50))

    def update(self, key, mouse):
        if mouse[1]:
            self.x_box.check_click()
            self.y_box.check_click()
        if key:
            self.x_box.poll(key)
            self.y_box.poll(key)
