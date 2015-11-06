import pygame


def draw_text(screen, font, text, color, position):
    screen.blit(font.render(text, True, color), pygame.Rect(position[0], position[1], font.size(text)[0],
                                                            font.size(text)[1]))
