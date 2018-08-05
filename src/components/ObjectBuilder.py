import pygame
import settings

from src.components.text.TextBox import TextBox
import src.const.Color as Color
import src.const.Font as Font


def back_button(x=settings.spacing, y=settings.spacing):
    return TextBox(pygame.Rect(x, y, 50, 30), Color.D_GRAY,
                   border_color=None,
                   highlight_color=Color.BLUE,
                   active_color=None, message="< <",
                   text_color=Color.WHITE,
                   font=Font.KAITI_M)


def cp_button(x=0, y=0, width=250, height=45, message=''):
    return TextBox(rect=pygame.Rect(x, y, width, height),
                   box_color=Color.D_GRAY,
                   highlight_color=Color.WHITE,
                   message=message,
                   text_color=Color.WHITE,
                   text_outline=True,
                   font=Font.KAITI_M)
