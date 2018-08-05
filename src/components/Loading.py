import pygame
import settings
import src.const.Color as Color
import src.const.Font as Font
from src.components.text.TextBox import TextBox


def loading_screen(screen):
    box = TextBox(rect=pygame.Rect(settings.screen_width/3, settings.screen_height/2-30, settings.screen_width/3, 60),
                  box_color=Color.BLACK,
                  border_color=Color.WHITE,
                  highlight_color=None,
                  active_color=None,
                  border=2,
                  highlight_box=False,
                  name="load_screen",
                  message="LOADING...",
                  text_color=Color.WHITE,
                  text_outline=True,
                  font=Font.KAITI_L)
    box.draw(screen=screen)
    pygame.display.flip()
