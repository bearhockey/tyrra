import pygame
import os
import re

# init pygame here because it needs to be initialized before anything else
pygame.init()

# calculate sizes of things
# screen_size = width, height = (640, 400)  # SNES view
# screen_size = width, height = (800, 480)  # mobile view
screen_size = screen_width, screen_height = (1024, 576)  # desktop view
spacing = int(screen_height/100)

huge_font_size = 40
big_font_size = 20
small_font_size = 14

script = os.path.abspath(os.path.realpath(__file__))
main_path = re.sub("settings\.pyc?", '', script)
src_path = os.path.join(main_path, "src")
res_path = os.path.join(main_path, "res")
face_path = os.path.join(res_path, "face")
data_path = os.path.join(main_path, "data")
mod_path = os.path.join(main_path, "mod")
