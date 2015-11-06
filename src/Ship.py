import pygame

import Color
import Text

from Box import Box
from InputBox import InputBox
from ShipNode import ShipNode


class Ship(object):
    def __init__(self, size_x=16, size_y=16):
        self.number = {
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5
        }

        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)

        self.main_window_pos = (20, 50)
        self.ship_window = self.main_window = Box(pygame.Rect(self.main_window_pos[0], self.main_window_pos[1],
                                                              800, 600),
                                                  box_color=None,
                                                  border_color=Color.white)
        self.main_screen = pygame.Surface(size=(800, 600))
        self.main_window_active = True
        self.name = InputBox(pygame.Rect(900, 50, 200, 50), box_color=None, border_color=Color.white, message='Tyrra',
                             text_color=Color.white, font=self.font, text_limit=16)

        # self.name = 'Tyrra'
        self.scrolling = False
        self.starting_scroll_pos = None
        self.starting_mouse_pos = None

        self.cell_size = 4
        self.grid = []
        for x in range(0, size_x):
            self.grid.append([])
            for y in range(0, size_y):
                self.grid[x].append(ShipNode(x, y, cell_size=16))
        self.grid_offset = (25, 55)

        self.mass_set(self.grid_offset[0], self.grid_offset[1], 4)

    def mass_move(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.move(x, y, zoom)

    def mass_set(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.set(x, y, zoom)

    def update(self, key, mouse):
        if key:
            if key == pygame.K_LEFT:
                self.mass_move(-8, 0)
            elif key == pygame.K_RIGHT:
                self.mass_move(8, 0)
            if key == pygame.K_UP:
                self.mass_move(0, -8)
            elif key == pygame.K_DOWN:
                self.mass_move(0, 8)

            if key in self.number:
                self.mass_move(0, 0, self.number[key])

            self.name.poll(key)
        if mouse:
            if self.main_window.check_click():
                self.main_window_active = True
                self.main_window.border_color = Color.white
            else:
                self.main_window_active = False
                self.main_window.border_color = (120, 120, 120)
            if mouse[1] or mouse[2]:
                self.name.check_click(offset=self.main_window_pos)
                if self.main_window_active:
                    for row in self.grid:
                        for node in row:
                            if node.update(mouse, offset=self.main_window_pos):
                                break
            elif mouse[3]:
                if not self.scrolling:
                    self.starting_mouse_pos = pygame.mouse.get_pos()
                    self.starting_scroll_pos = self.grid_offset
                self.scrolling = True
                new_pos_x = pygame.mouse.get_pos()[0] - self.starting_mouse_pos[0]
                new_pos_y = pygame.mouse.get_pos()[1] - self.starting_mouse_pos[1]
                self.grid_offset = (self.starting_scroll_pos[0] + new_pos_x, self.starting_scroll_pos[1] + new_pos_y)
                if self.main_window_active:
                    self.mass_set(self.grid_offset[0], self.grid_offset[1])
            else:
                self.scrolling = False

    def draw(self, screen):
        self.name.draw(screen)
        # Text.draw_text(screen, self.font, self.name, Color.white, (900, 50))
        self.main_screen.fill(Color.black)
        for row in self.grid:
            for node in row:
                node.draw(self.main_screen)
        screen.blit(self.main_screen, self.main_window_pos)
        self.ship_window.draw(screen)

        # ship preview
        position = (880, 370)
        size = 8
        pygame.draw.rect(screen, Color.white, pygame.Rect(position[0], position[1], len(self.grid)*size,
                                                          len(self.grid[0])*size), 2)
        for row in self.grid:
            for node in row:
                if node.type:
                    pygame.draw.rect(screen, Color.white, pygame.Rect(position[0] + node.cell_x*size,
                                                                      position[1] + node.cell_y*size,
                                                                      size, size))
