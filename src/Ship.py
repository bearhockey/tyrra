import json
import pygame

import Color

from Box import Box
from InputBox import InputBox
from ShipNode import ShipNode
from TextBox import TextBox


class Ship(object):
    def __init__(self, size_x=16, size_y=16):
        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.match_font('kaiti'), self.small_font_size)
        self.name = 'Tyrra'

        self.ship_grid = ShipGrid(size_x, size_y)
        self.ship_preview = self.ship_grid.preview_window

        # objects are drawn on side bar
        self.name_box = InputBox(pygame.Rect(50, 10, 250, 50), box_color=None, border_color=Color.d_gray,
                                 highlight_color=Color.white, active_color=Color.gray, message=self.name,
                                 text_color=Color.white, font=self.font, text_limit=16)

        # floors
        self.floor_text = TextBox(pygame.Rect(40, 75, 100, 25), box_color=None, border_color=None, highlight_color=None,
                                  active_color=None, message='Floors:', text_color=Color.white, text_outline=True,
                                  font=self.small_font)
        self.floor_dictionary = {'blank': 0,
                                 'floor': 1,
                                 'armor': 2,
                                 'thruster': 3}
        self.floors = []
        self.floors.append(Box(pygame.Rect(40, 100, 25, 25), Color.black, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='blank'))
        self.floors.append(Box(pygame.Rect(70, 100, 25, 25), Color.gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='floor'))
        self.floors.append(Box(pygame.Rect(100, 100, 25, 25), Color.d_gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='armor'))
        self.ship_grid.selected_cell_type = self.floor_dictionary['blank']

        # components
        # self.ship_components = []
        self.floors.append(TextBox(pygame.Rect(40, 150, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='thruster',
                                   message='T', text_color=Color.blue, text_outline=True, font=self.small_font))

        # debug load button
        self.load_box = TextBox(pygame.Rect(50, 350, 70, 40), Color.blue, border_color=Color.gray,
                                highlight_color=Color.white, active_color=Color.white, message='LOAD',
                                text_color=Color.white, text_outline=True, font=self.font)
        # debug save button
        self.save_box = TextBox(pygame.Rect(150, 350, 70, 40), Color.red, border_color=Color.gray,
                                highlight_color=Color.white, active_color=Color.white, message='SAVE',
                                text_color=Color.white, text_outline=True, font=self.font)

    def update(self, key, mouse, offset=(0, 0)):
        self.name_box.update(key, mouse, offset)
        for tile in self.floors:
            tile.update(key, mouse, offset)
            if tile.active:
                self.ship_grid.selected_cell_type = self.floor_dictionary[tile.name]
        if self.load_box.update(key, mouse, offset):
            self.load('../data/test.txt')
        if self.save_box.update(key, mouse, offset):
            self.save('../data/test.txt')

    def draw(self, screen):
        screen.fill(Color.black)
        self.name_box.draw(screen)
        self.floor_text.draw(screen)
        for tile in self.floors:
            tile.draw(screen)

        self.load_box.draw(screen)
        self.save_box.draw(screen)
        self.ship_preview.draw(screen)

    def load(self, file_name):
        with open(file_name) as data_file:
            data = json.load(data_file)
        self.name_box.message = data['NAME']
        index = 0
        for row in self.ship_grid.grid:
            for node in row:
                node.type = data['GRID'][index]
                index += 1

    def save(self, file_name):
        dump = {'NAME': self.name_box.message}
        grid = []
        for row in self.ship_grid.grid:
            for node in row:
                grid.append(node.type)
        dump['GRID'] = grid
        with open(file_name, 'w') as outfile:
            json.dump(dump, outfile)
        print 'saved to file'


class ShipPreview(object):
    def __init__(self, ship, position, size, zoom=2, padding=0):
        self.ship_grid = ship
        self.position = position
        self.size = size
        self.zoom = zoom
        self.padding = padding

    def draw(self, screen):
        pygame.draw.rect(screen, Color.black, pygame.Rect(self.position[0], self.position[1], self.size[0],
                                                          self.size[1]))
        pygame.draw.rect(screen, Color.white, pygame.Rect(self.position[0], self.position[1], self.size[0],
                                                          self.size[1]), 2)

        w_offset = len(self.ship_grid.grid[0]) - \
            (self.ship_grid.ship_bounds['right'] - self.ship_grid.ship_bounds['left'])
        h_offset = len(self.ship_grid.grid) - (self.ship_grid.ship_bounds['bottom'] - self.ship_grid.ship_bounds['top'])
        x = 0
        for row in self.ship_grid.grid[self.ship_grid.ship_bounds['left']:self.ship_grid.ship_bounds['right']+1]:
            y = 0
            for node in row[self.ship_grid.ship_bounds['top']:self.ship_grid.ship_bounds['bottom']+1]:
                if node.type is not 0:
                    pygame.draw.rect(screen, Color.white,
                                     pygame.Rect(self.padding + w_offset + self.position[0] + x * self.zoom,
                                                 self.padding + h_offset + self.position[1] + y * self.zoom,
                                                 self.zoom, self.zoom))
                y += 1
            x += 1


class ShipGrid(object):
    def __init__(self, size_x=16, size_y=16):
        self.number = {
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5
        }

        self.main_window_active = True

        self.ship_bounds = {'top': 0,
                            'left': 0,
                            'bottom': size_y-1,
                            'right': size_x-1}

        self.scrolling = False
        self.starting_scroll_pos = None
        self.starting_mouse_pos = None

        self.selected_cell_type = 0

        self.cell_size = 4
        self.grid = []
        for x in range(0, size_x):
            self.grid.append([])
            for y in range(0, size_y):
                self.grid[x].append(ShipNode(x, y, cell_size=16))
        self.grid_offset = (25, 55)
        self.zoom_level = 1

        self.mass_set(self.grid_offset[0], self.grid_offset[1], self.zoom_level)

        self.preview_window = ShipPreview(self, (75, 425), (200, 200), zoom=4, padding=20)

    def mass_move(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.move(x, y, zoom)

    def mass_set(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.set(x, y, zoom)

    def update(self, key, mouse, offset=(0, 0)):
        if key:
            if key == pygame.K_LEFT:
                self.mass_move(-8, 0)
            elif key == pygame.K_RIGHT:
                self.mass_move(8, 0)
            if key == pygame.K_UP:
                self.mass_move(0, -8)
            elif key == pygame.K_DOWN:
                self.mass_move(0, 8)

        if mouse is not None:
            if mouse[1] or mouse[2]:
                for row in self.grid:
                    for node in row:
                        if node.update(mouse=mouse, floor_type=self.selected_cell_type, offset=offset):
                            break
            elif mouse[4]:
                self.zoom_level += 1
                self.mass_move(0, 0, self.zoom_level)
            elif mouse[5]:
                self.zoom_level -= 1
                if self.zoom_level < 1:
                    self.zoom_level = 1
                self.mass_move(0, 0, self.zoom_level)
            if mouse[3]:
                if not self.scrolling:
                    self.starting_mouse_pos = pygame.mouse.get_pos()
                    self.starting_scroll_pos = self.grid_offset
                    print self.starting_scroll_pos
                self.scrolling = True
                new_pos_x = pygame.mouse.get_pos()[0] - self.starting_mouse_pos[0]
                new_pos_y = pygame.mouse.get_pos()[1] - self.starting_mouse_pos[1]
                self.grid_offset = (self.starting_scroll_pos[0] + new_pos_x, self.starting_scroll_pos[1] + new_pos_y)
                self.mass_set(self.grid_offset[0], self.grid_offset[1])
            else:
                self.scrolling = False
        else:
            self.scrolling = False

        # get ship bounds
        x_index = 0
        left_bound = len(self.grid)
        top_bound = len(self.grid[0])
        right_bound = 0
        bottom_bound = 0
        for row in self.grid:
            y_index = 0
            for node in row:
                if node.type > 0:
                    if x_index < left_bound:
                        left_bound = x_index
                    if x_index > right_bound:
                        right_bound = x_index
                    if y_index < top_bound:
                        top_bound = y_index
                    if y_index > bottom_bound:
                        bottom_bound = y_index
                y_index += 1
            x_index += 1

        self.ship_bounds['left'] = left_bound
        self.ship_bounds['top'] = top_bound
        self.ship_bounds['right'] = right_bound
        self.ship_bounds['bottom'] = bottom_bound
        self.preview_window.ship_grid = self
        # print left_bound, top_bound, right_bound, bottom_bound

    def draw(self, screen):
        screen.fill(Color.black)
        for row in self.grid:
            for node in row:
                node.draw(screen)
