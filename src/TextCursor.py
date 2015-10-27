import pygame


class TextCursor(object):
    def __init__(self):
        pass

    @staticmethod
    def draw(screen, position, font, color=None):
        # janky way to make cursor blink
        time = pygame.time.get_ticks()
        if time % 1000 < 500:
            cursor_color = color
            if color is None:
                cursor_color = (255, 255, 255)
            length = font.get_linesize()

            pygame.draw.line(screen, cursor_color, position, (position[0], position[1]+length), 2)
