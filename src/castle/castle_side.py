import pygame
import src.Color as Color
from src.components.text import Text


class CastleSideBar(object):
    def __init__(self, player_character, font, small_font):
        self.font = font
        self.small_font = small_font
        self.pc = player_character
        self.port_rect = pygame.Rect(15, 15, 250, 250)

    def draw(self, screen):
        # draw portrait
        if self.pc.portrait:
            screen.blit(self.pc.portrait, self.port_rect)
            pygame.draw.rect(screen, Color.d_gray,
                             (self.port_rect.left + 1,
                              self.port_rect.top + 1,
                              self.port_rect.width,
                              self.port_rect.height), 2)
            pygame.draw.rect(screen, Color.white, self.port_rect, 2)
        # draw health
        Text.draw_text(screen,
                       self.font,
                       "{0} / {1} HP".format(self.pc.hp, self.pc.stats["HP"]),
                       Color.green, (75, 300))
