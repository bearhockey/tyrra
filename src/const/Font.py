# Fonts go here
import pygame
import settings
from os.path import join

KAITI_L = pygame.font.Font(join(settings.res_path, "kaiti.ttf"), settings.huge_font_size)
KAITI_M = pygame.font.Font(join(settings.res_path, "kaiti.ttf"), settings.big_font_size)
KAITI_S = pygame.font.Font(join(settings.res_path, "kaiti.ttf"), settings.small_font_size)
