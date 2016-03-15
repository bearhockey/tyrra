import json
import pygame

import Color
import Text

from Box import Box
from InputBox import InputBox
from Pawn import Pawn
from ShipNode import ShipNode
from TextBox import TextBox


class Ship(object):
    def __init__(self, size_x=16, size_y=16):
        self.big_font_size = 24
        self.small_font_size = 16
        self.font = pygame.font.Font(pygame.font.match_font('kaiti'), self.big_font_size)
        self.small_font = pygame.font.Font(pygame.font.match_font('kaiti'), self.small_font_size)
        self.name = 'Tyrra'
        self.crew = [Pawn()]

        self.panel_mode = 'stats'
        self.ship_grid = ShipGrid(self, size_x, size_y)
        self.ship_preview = self.ship_grid.preview_window
        self.crew_profile = CrewProfile(self, self.crew[0], self.font, self.small_font)
        self.main_screen = ShipMainScreen(Box(pygame.Rect(0, 0, 10, 10), box_color=Color.white), self.ship_grid,
                                          self.crew_profile)
        self.box = Box(self.get_ship_rect(), border_color=Color.blue, highlight_color=Color.green,
                       active_color=Color.red, name='Ship Hit Box')
        # easy dictionary to store stats probably
        self.ship_stats = {'crew_capacity': 1,
                           'attack': 0,
                           'armor': 0,
                           'speed': 0,
                           'power': 0}

        # objects are drawn on side bar
        self.name_box = InputBox(pygame.Rect(70, 10, 250, 50), box_color=None, border_color=Color.d_gray,
                                 highlight_color=Color.white, active_color=Color.gray, message=self.name,
                                 text_color=Color.white, font=self.font, text_limit=16)

        # nav
        self.stats_button = TextBox(pygame.Rect(25, 70, 80, 30), box_color=Color.d_gray, border_color=Color.gray,
                                    highlight_color=Color.white, active_color=Color.d_blue, message='Stats',
                                    text_color=Color.white, text_outline=True, font=self.font)
        self.edit_button = TextBox(pygame.Rect(120, 70, 80, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.d_blue, message='Edit',
                                   text_color=Color.white, text_outline=True, font=self.font)
        self.crew_button = TextBox(pygame.Rect(210, 70, 80, 30), box_color=Color.d_gray, border_color=Color.gray,
                                   highlight_color=Color.white, active_color=Color.d_blue, message='Crew',
                                   text_color=Color.white, text_outline=True, font=self.font)

        # floors
        self.floor_text = TextBox(pygame.Rect(25, 110, 100, 25), box_color=None, border_color=None,
                                  highlight_color=None, active_color=None, message='Floors:', text_color=Color.white,
                                  text_outline=True, font=self.small_font)
        self.floor_dictionary = {'blank': 0,
                                 'floor': 1,
                                 'armor': 2,
                                 'engine': 3,
                                 'gun': 4,
                                 'power': 5}
        self.floor_stats = {'blank': (0, 0, 0, 0),
                            'floor': (0, -1, -1, -1),
                            'armor': (0, 10, -2, 0),
                            'engine': (0, 0, 10, -5),
                            'gun': (10, 0, -1, -5),
                            'power': (0, 0, -1, 10)}

        self.floors = []
        self.floors.append(Box(pygame.Rect(25, 140, 25, 25), Color.black, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='blank'))
        self.floors.append(Box(pygame.Rect(55, 140, 25, 25), Color.gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='floor'))
        self.floors.append(Box(pygame.Rect(85, 140, 25, 25), Color.d_gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='armor'))
        self.ship_grid.selected_cell_type = self.floor_dictionary['blank']

        # some text
        self.attack_text = TextBox(pygame.Rect(230, 425, 50, 50), message='Attack:', text_color=Color.red,
                                   font=self.small_font)
        self.attack_value = TextBox(pygame.Rect(300, 425, 50, 50), message='', text_color=Color.red,
                                    font=self.small_font)
        self.armor_text = TextBox(pygame.Rect(230, 455, 50, 50), message='Armor:', text_color=Color.gray,
                                  font=self.small_font)
        self.armor_value = TextBox(pygame.Rect(300, 455, 50, 50), message='', text_color=Color.gray,
                                   font=self.small_font)
        self.speed_text = TextBox(pygame.Rect(230, 485, 50, 50), message='Speed:', text_color=Color.blue,
                                  font=self.small_font)
        self.speed_value = TextBox(pygame.Rect(300, 485, 50, 50), message='', text_color=Color.blue,
                                   font=self.small_font)
        self.power_text = TextBox(pygame.Rect(230, 515, 50, 50), message='Power:', text_color=Color.green,
                                  font=self.small_font)
        self.power_value = TextBox(pygame.Rect(300, 515, 50, 50), message='', text_color=Color.green,
                                   font=self.small_font)

        # components
        self.floors.append(TextBox(pygame.Rect(25, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='engine',
                                   message='E1', text_color=Color.blue, text_outline=True, font=self.small_font))
        self.floors.append(TextBox(pygame.Rect(55, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='gun',
                                   message='G1', text_color=Color.red, text_outline=True, font=self.small_font))
        self.floors.append(TextBox(pygame.Rect(85, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='power',
                                   message='P1', text_color=Color.green, text_outline=True, font=self.small_font))

        # debug load button
        self.load_box = TextBox(pygame.Rect(230, 545, 75, 40), Color.blue, border_color=Color.gray,
                                highlight_color=Color.white, active_color=Color.white, message='LOAD',
                                text_color=Color.white, text_outline=True, font=self.font)
        # debug save button
        self.save_box = TextBox(pygame.Rect(230, 585, 75, 40), Color.red, border_color=Color.gray,
                                highlight_color=Color.white, active_color=Color.white, message='SAVE',
                                text_color=Color.white, text_outline=True, font=self.font)

        # crew screen
        self.crew_list = []
        self.make_crew_list()

    def add_crew(self, crew):
        self.crew.append(crew)
        self.make_crew_list()
        self.crew_profile.pawn = self.crew[0]

    def make_crew_list(self):
        del self.crew_list[:]
        y_offset = 0
        for pawn in self.crew:
            self.crew_list.append(TextBox(pygame.Rect(50, 150+y_offset, 250, 40), box_color=Color.gray,
                                          border_color=Color.d_gray, highlight_color=Color.white,
                                          active_color=Color.blue, border=2, message=pawn.name, text_color=Color.white,
                                          text_outline=True, font=self.font))
            y_offset += 55

    def update(self, key, mouse, offset=(0, 0)):
        self.name_box.update(key, mouse, offset)
        if self.stats_button.update(key, mouse, offset):
            self.panel_mode = 'stats'
            self.main_screen.mode = 'stats'
        if self.edit_button.update(key, mouse, offset):
            self.panel_mode = 'edit'
            self.main_screen.mode = 'edit'
        if self.crew_button.update(key, mouse, offset):
            self.panel_mode = 'crew'
            self.main_screen.mode = 'crew'

        if self.panel_mode is 'edit':
            self.update_edit_panel(key, mouse, offset)
        elif self.panel_mode is 'crew':
            self.update_crew_panel(key, mouse, offset)
            # self.ship_grid.update(key=key, mouse=mouse)

        # get stats
        self.update_stats()

    def update_edit_panel(self, key, mouse, offset=(0, 0)):
        for tile in self.floors:
            tile.update(key, mouse, offset)
            if tile.active:
                self.ship_grid.selected_cell_type = self.floor_dictionary[tile.name]
                self.ship_grid.selected_cell_stats = self.floor_stats[tile.name]
        if self.load_box.update(key, mouse, offset):
            self.load('data/save.shp')
        if self.save_box.update(key, mouse, offset):
            self.save('data/save.shp')

    def update_crew_panel(self, key, mouse, offset=(0, 0)):
        for crew in self.crew_list:
            if crew.update(key, mouse, offset):
                for pawn in self.crew:
                    if pawn.name == crew.message:
                        if self.crew_profile is not None:
                            self.crew_profile.pawn = pawn
                        break

    def update_stats(self):
        attack, armor, speed, power = self.ship_grid.get_stats()
        self.ship_stats['attack'] = attack
        self.ship_stats['armor'] = armor
        self.ship_stats['speed'] = speed
        self.ship_stats['power'] = power
        self.attack_value.message = str(attack)
        self.armor_value.message = str(armor)
        self.speed_value.message = str(speed)
        self.power_value.message = str(power)

    def draw(self, screen):
        screen.fill(Color.black)
        self.name_box.draw(screen)
        self.stats_button.draw(screen)
        self.edit_button.draw(screen)
        self.crew_button.draw(screen)

        if self.panel_mode is 'edit':
            self.draw_edit_panel(screen)
        elif self.panel_mode is 'crew':
            self.draw_crew_panel(screen)

    def draw_crew_panel(self, screen):
        for box in self.crew_list:
            box.draw(screen)

    def draw_edit_panel(self, screen):
        self.floor_text.draw(screen)
        for tile in self.floors:
            tile.draw(screen)

        self.load_box.draw(screen)
        self.save_box.draw(screen)

        self.attack_text.draw(screen)
        self.attack_value.draw(screen)
        self.armor_text.draw(screen)
        self.armor_value.draw(screen)
        self.speed_text.draw(screen)
        self.speed_value.draw(screen)
        self.power_text.draw(screen)
        self.power_value.draw(screen)

        self.ship_preview.draw_border(screen)
        self.ship_preview.draw(screen)

    def draw_ship(self, screen, position, color=None, zoom=2):
        if color is None:
            color = Color.white
        self.box.rect = self.get_ship_rect(position=position, zoom=zoom)
        # self.ship_grid.update_bounds()
        x = 0
        for row in self.ship_grid.grid[self.ship_grid.ship_bounds['left']:self.ship_grid.ship_bounds['right']+1]:
            y = 0
            for node in row[self.ship_grid.ship_bounds['top']:self.ship_grid.ship_bounds['bottom']+1]:
                if node.type is not 0:
                    pygame.draw.rect(screen, color,
                                     pygame.Rect(position[0] + x*zoom, position[1] + y*zoom, zoom, zoom))
                y += 1
            x += 1
        # self.box.draw(screen)

    def get_ship_rect(self, position=None, zoom=1):
        self.ship_grid.update_bounds()
        if position is None:
            position = (0, 0)
        return pygame.Rect(position[0], position[1],
                           (self.ship_grid.ship_bounds['right'] - self.ship_grid.ship_bounds['left'] + 1) * zoom,
                           (self.ship_grid.ship_bounds['bottom'] - self.ship_grid.ship_bounds['top'] + 1) * zoom)

    def load(self, file_name):
        with open(file_name) as data_file:
            data = json.load(data_file)
        self.name_box.message = data['NAME']
        index = 0
        for row in self.ship_grid.grid:
            for node in row:
                node.type = data['GRID'][index][0]
                node.set_stats(data['GRID'][index][1])
                index += 1
        self.update_stats()

    def save(self, file_name):
        dump = {'NAME': self.name_box.message}
        grid = []
        for row in self.ship_grid.grid:
            for node in row:
                grid.append((node.type, node.get_stats()))
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

    def draw_border(self, screen):
        pygame.draw.rect(screen, Color.black, pygame.Rect(self.position[0], self.position[1], self.size[0],
                                                          self.size[1]))
        pygame.draw.rect(screen, Color.white, pygame.Rect(self.position[0], self.position[1], self.size[0],
                                                          self.size[1]), 2)

    def draw(self, screen, position=None, color=None):
        if position is None:
            position = self.position
        if color is None:
            color = Color.white
        w_offset = len(self.ship_grid.grid[0]) - \
            (self.ship_grid.ship_bounds['right'] - self.ship_grid.ship_bounds['left'])
        h_offset = len(self.ship_grid.grid) - (self.ship_grid.ship_bounds['bottom'] - self.ship_grid.ship_bounds['top'])

        self.ship_grid.ship.draw_ship(screen, position=(position[0] + w_offset, position[1] + h_offset),
                                      color=color, zoom=4)


class ShipMainScreen(object):
    def __init__(self, stats, grid, crew):
        self.mode = 'stats'
        self.stats = stats
        self.grid = grid
        self.crew = crew

    def update(self, key, mouse, offset=(0, 0)):
        if self.mode is 'edit':
            self.grid.update(key=key, mouse=mouse, offset=offset)
        elif self.mode is 'crew':
            self.crew.update(key=key, mouse=mouse, offset=offset)

    def draw(self, screen):
        if self.mode is 'stats':
            self.stats.draw(screen)
        elif self.mode is 'edit':
            self.grid.draw(screen)
        elif self.mode is 'crew':
            if self.crew is not None:
                self.crew.draw(screen)


class ShipGrid(object):
    def __init__(self, ship, size_x=16, size_y=16):
        self.ship = ship
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
        self.selected_cell_stats = (0, 0, 0, 0)

        self.cell_size = 4
        self.grid = []
        for x in range(0, size_x):
            self.grid.append([])
            for y in range(0, size_y):
                self.grid[x].append(ShipNode(x, y, cell_size=16))
        self.grid_offset = (25, 55)
        self.zoom_level = 1

        self.mass_set(self.grid_offset[0], self.grid_offset[1], self.zoom_level)

        self.preview_window = ShipPreview(self, (20, 425), (200, 200), zoom=4, padding=20)

    def mass_move(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.move(x, y, zoom)

    def mass_set(self, x, y, zoom=None):
        for row in self.grid:
            for node in row:
                node.set(x, y, zoom)

    def get_stats(self):
        attack = 0
        armor = 0
        speed = 0
        power = 0
        for row in self.grid:
            for node in row:
                attack += node.attack
                armor += node.armor
                speed += node.speed
                power += node.power

        return attack, armor, speed, power

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
                            node.set_stats(self.selected_cell_stats)
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
                self.scrolling = True
                new_pos_x = pygame.mouse.get_pos()[0] - self.starting_mouse_pos[0]
                new_pos_y = pygame.mouse.get_pos()[1] - self.starting_mouse_pos[1]
                self.grid_offset = (self.starting_scroll_pos[0] + new_pos_x, self.starting_scroll_pos[1] + new_pos_y)
                self.mass_set(self.grid_offset[0], self.grid_offset[1])
            else:
                self.scrolling = False
        else:
            self.scrolling = False
        self.update_bounds()
        self.preview_window.ship_grid = self

    def update_bounds(self):
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

    def draw(self, screen):
        screen.fill(Color.black)
        for row in self.grid:
            for node in row:
                node.draw(screen)


class CrewProfile(object):
    def __init__(self, ship, pawn, font, small_font):
        self.ship = ship
        self.pawn = pawn
        self.font = font
        self.small_font = small_font

    def draw(self, screen):
        port_rect = pygame.Rect(25, 25, 250, 250)
        if self.pawn.portrait:
            screen.blit(self.pawn.portrait, port_rect)
        else:
            Text.draw_text(screen, self.small_font, 'No portrtait avilable', Color.red, (75, 125))
        pygame.draw.rect(screen, Color.d_gray,
                         (port_rect.left+1, port_rect.top+1, port_rect.width, port_rect.height), 2)
        pygame.draw.rect(screen, Color.white, port_rect, 2)
        Text.draw_text(screen, self.font, 'NAME:', Color.white, (300, 50))
        Text.draw_text(screen, self.font, self.pawn.name, Color.white, (400, 50))
        Text.draw_text(screen, self.font, 'AGE:', Color.white, (300, 80))
        Text.draw_text(screen, self.font, str(self.pawn.age), Color.white, (400, 80))
        Text.draw_text(screen, self.font, 'RACE:', Color.white, (300, 110))
        Text.draw_text(screen, self.font, self.pawn.race, Color.white, (400, 110))
        Text.draw_text(screen, self.font, 'BIO:', Color.white, (300, 150))
        Text.draw_text(screen, self.small_font, self.pawn.bio, Color.white, (300, 180), width=400)

        Text.draw_text(screen, self.font, 'JOBS', Color.white, (25, 300))
        y = 350
        for skill, value in self.pawn.ship_skills.iteritems():
            Text.draw_text(screen, self.small_font, '{0}:'.format(skill), Color.white, (25, y))
            Text.draw_text(screen, self.small_font, str(value), Color.white, (125, y))
            y += 30
        Text.draw_text(screen, self.font, 'STATS', Color.white, (225, 300))
        y = 350
        for stat, value in self.pawn.battle_skills.iteritems():
            Text.draw_text(screen, self.small_font, '{0}:'.format(stat), Color.white, (225, y))
            Text.draw_text(screen, self.small_font, str(value), Color.white, (325, y))
            y += 30

    def update(self, key, mouse, offset=(0, 0)):
        pass
