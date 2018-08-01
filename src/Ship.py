import json

import pygame

import src.Color as Color
import settings
from src.Component import Component
from src.Pawn import Pawn
from src.ShipNode import ShipNode
from src.components.text import Text
from src.components.Box import Box
from src.components.text.InputBox import InputBox
from src.components.text.TextBox import TextBox


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
        self.stat_screen = ShipStats(self, self.font, self.small_font)
        self.crew_profile = CrewProfile(self, self.crew[0], self.font, self.small_font)
        self.main_screen = ShipMainScreen(self.stat_screen, self.ship_grid, self.crew_profile)
        self.box = Box(self.get_ship_rect(), border_color=Color.blue, highlight_color=Color.green,
                       active_color=Color.red, name='Ship Hit Box')
        # easy dictionary to store stats probably
        self.ship_stats = {'crew_capacity': 1,
                           'attack': 0,
                           'armor': 0,
                           'speed': 0,
                           'power': 0,
                           'shield': 0,
                           'component_capacity': 4}
        self.current_shield = 0

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
        self.floor_dictionary = {'blank': 0,
                                 'floor': 1,
                                 'armor': 2,
                                 'engine': 3,
                                 'gun': 4,
                                 'power': 5,
                                 'shield': 7}
        self.floor_stats = {'blank': (0, 0, 0, 0),
                            'floor': (0, -1, -1, -1),
                            'armor': (0, 10, -2, 0),
                            'engine': (0, 0, 10, -5),
                            'gun': (10, 0, -1, -5),
                            'power': (0, 0, -1, 10),
                            'shield': (0, 0, 0, -10)}

        self.floors = []
        self.floors.append(Box(pygame.Rect(25, 140, 25, 25), Color.black, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='blank'))
        self.floors.append(Box(pygame.Rect(55, 140, 25, 25), Color.gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='floor'))
        self.floors.append(Box(pygame.Rect(85, 140, 25, 25), Color.d_gray, border_color=Color.d_gray,
                               highlight_color=Color.white, active_color=Color.blue, border=1, name='armor'))
        self.ship_grid.selected_cell_type = self.floor_dictionary['blank']

        # Parts
        self.floors.append(TextBox(pygame.Rect(25, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='engine',
                                   message='E1', text_color=Color.blue, text_outline=True, font=self.small_font))
        self.floors.append(TextBox(pygame.Rect(55, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='gun',
                                   message='G1', text_color=Color.red, text_outline=True, font=self.small_font))
        self.floors.append(TextBox(pygame.Rect(85, 180, 25, 25), Color.black, border_color=Color.d_gray,
                                   highlight_color=Color.white, active_color=Color.blue, border=1, name='power',
                                   message='P1', text_color=Color.green, text_outline=True, font=self.small_font))

        # components (inventory / installed are actual objects; lists are just the text boxes)
        self.selected_component = None
        self.component_inventory = []
        self.component_list = []
        self.installed_components = []
        self.installed_list = []
        self.make_installed_component_list()

        # debug load button
        self.load_box = TextBox(pygame.Rect(230, 610, 75, 40), Color.blue, border_color=Color.gray,
                                highlight_color=Color.white, active_color=Color.white, message='LOAD',
                                text_color=Color.white, text_outline=True, font=self.font)
        # debug save button
        self.save_box = TextBox(pygame.Rect(230, 650, 75, 40), Color.red, border_color=Color.gray,
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

    def add_component(self, component):
        self.component_inventory.append(component)
        self.make_component_list()

    def make_component_list(self):
        del self.component_list[:]
        y_offset = 0
        for component in self.component_inventory:
            self.component_list.append(TextBox(pygame.Rect(25, 150+y_offset, 250, 40), box_color=Color.d_gray,
                                               border_color=Color.gray, highlight_color=Color.red,
                                               active_color=Color.gray, border=2,
                                               name=self.component_inventory.index(component), message=component.name,
                                               text_color=Color.white, text_outline=True, font=self.font))
            y_offset += 55

    def install_component(self, index):
        if self.component_inventory[index].component_type is not 'empty':
            self.installed_components.append(index)
        self.make_installed_component_list()

    def remove_component(self, index):
        if len(self.installed_components) > index:
            del self.installed_components[index]
            self.make_installed_component_list()

    def make_installed_component_list(self):
        del self.installed_list[:]
        for i in range(1, self.ship_stats['component_capacity'] + 1):
            if len(self.installed_components) > i - 1:
                index = self.installed_components[i - 1]
                self.installed_list.append(TextBox(pygame.Rect(25, 250 + ((i - 1) * 50), 300, 40), Color.d_gray,
                                                   border_color=Color.gray, highlight_color=Color.white,
                                                   active_color=Color.blue, border=2, name=i,
                                                   message=self.component_inventory[index].name, text_color=Color.gray,
                                                   text_outline=True, font=self.font))
            else:
                self.installed_list.append(TextBox(pygame.Rect(25, 250+((i-1)*50), 300, 40), Color.d_gray,
                                                   border_color=Color.gray, highlight_color=Color.white,
                                                   active_color=Color.blue, border=2, name=i,
                                                   message='EMPTY {0}'.format(i), text_color=Color.gray,
                                                   text_outline=True, font=self.font))

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

        if self.panel_mode is 'component':
            self.update_component_panel(key, mouse, offset)
        elif self.panel_mode is 'edit':
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

        for component in self.installed_list:
            if component.update(key, mouse, offset):
                self.selected_component = component.name-1
                self.panel_mode = 'component'

        if self.load_box.update(key, mouse, offset):
            self.load('{0}data/save.shp'.format(settings.main_path))
        if self.save_box.update(key, mouse, offset):
            self.save('{0}data/save.shp'.format(settings.main_path))

    def update_component_panel(self, key, mouse, offset=(0, 0)):
        for component in self.component_list:
            if len(self.component_inventory) > 0:
                index = int(component.name)
            else:
                index = 0
            if index not in self.installed_components:
                if component.update(key, mouse, offset):
                    print("index is {0}".format(index))
                    self.remove_component(index)
                    self.install_component(index)
                    self.panel_mode = 'edit'

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
        self.ship_stats['shield'] = 0
        for index in self.installed_components:
            component = self.component_inventory[index]
            if component.stats:
                for stat, value in component.stats.iteritems():
                    if stat in self.ship_stats:
                        self.ship_stats[stat] += value
        # reset shield HP
        self.current_shield = self.ship_stats['shield']

    def draw(self, screen):
        screen.fill(Color.black)
        self.name_box.draw(screen)
        self.stats_button.draw(screen)
        self.edit_button.draw(screen)
        self.crew_button.draw(screen)

        if self.panel_mode is 'edit':
            self.draw_edit_panel(screen)
        elif self.panel_mode is 'component':
            self.draw_component_panel(screen)
        elif self.panel_mode is 'crew':
            self.draw_crew_panel(screen)

    def draw_crew_panel(self, screen):
        for box in self.crew_list:
            box.draw(screen)

    def draw_edit_panel(self, screen):
        Text.draw_text(screen, self.small_font, 'Floors:', Color.white, position=(25, 110))
        for tile in self.floors:
            tile.draw(screen)
        Text.draw_text(screen, self.small_font, 'Components:', Color.white, position=(25, 220))
        for box in self.installed_list:
            box.draw(screen)

        self.load_box.draw(screen)
        self.save_box.draw(screen)

        Text.draw_text(screen, self.small_font, 'Preview:', Color.white, position=(25, 460))

        Text.draw_text(screen, self.small_font, 'Attack:', Color.red, position=(230, 485))
        Text.draw_text(screen, self.small_font, self.ship_stats['attack'], Color.red, position=(300, 485))

        Text.draw_text(screen, self.small_font, 'Armor:', Color.gray, position=(230, 510))
        Text.draw_text(screen, self.small_font, self.ship_stats['armor'], Color.gray, position=(300, 510))

        Text.draw_text(screen, self.small_font, 'Speed:', Color.blue, position=(230, 535))
        Text.draw_text(screen, self.small_font, self.ship_stats['speed'], Color.blue, position=(300, 535))

        Text.draw_text(screen, self.small_font, 'Power:', Color.yellow, position=(230, 560))
        Text.draw_text(screen, self.small_font, self.ship_stats['power'], Color.yellow, position=(300, 560))

        Text.draw_text(screen, self.small_font, 'Shield:', Color.green, position=(230, 585))
        Text.draw_text(screen, self.small_font, self.ship_stats['shield'], Color.green, position=(300, 585))

        self.ship_preview.draw_border(screen)
        self.ship_preview.draw(screen)

    def draw_component_panel(self, screen):
        Text.draw_text(screen, self.small_font, 'Components:', Color.white, position=(25, 110))
        for component in self.component_list:
            component.draw(screen)

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
        return pygame.Rect(position[0], position[1], self.get_ship_size(zoom)[0], self.get_ship_size(zoom)[1])

    def get_ship_size(self, zoom=1):
        self.ship_grid.update_bounds()
        w = (self.ship_grid.ship_bounds['right'] - self.ship_grid.ship_bounds['left'] + 1) * zoom
        h = (self.ship_grid.ship_bounds['bottom'] - self.ship_grid.ship_bounds['top'] + 1) * zoom
        return w, h

    def load(self, file_name):
        try:
            with open(file_name) as data_file:
                data = json.load(data_file)
            self.name_box.message = data['NAME']
            index = 0
            for row in self.ship_grid.grid:
                for node in row:
                    node.type = data['GRID'][index][0]
                    node.set_stats(data['GRID'][index][1])
                    index += 1
            # components
            del self.component_inventory[:]
            self.make_component_list()
            self.add_component(Component('empty', name='REMOVE'))
            if "C_INV" in data:
                for inventory in data["C_INV"]:
                    self.add_component(Component(component_type=inventory["TYPE"],
                                                 name=inventory["NAME"],
                                                 stats=inventory["STATS"]))
            del self.installed_components[:]
            if "C_ACT" in data:
                self.installed_components = data["C_ACT"]
            self.make_installed_component_list()
            # crew
            del self.crew[:]
            if "CREW" in data:
                for crew in data["CREW"]:
                    self.add_crew(Pawn(name=crew["NAME"],
                                       age=crew["AGE"],
                                       race=crew["RACE"],
                                       bio=crew["BIO"],
                                       profile=crew["PICTURE"],
                                       ship_skills=crew["SKILLS"],
                                       battle_skills=crew["STATS"]))

            self.update_stats()
        except Exception as e:
            print("Failed to load ship file {0} : {1}".format(file_name, e))

    def save(self, file_name):
        dump = {'NAME': self.name_box.message}
        grid = []
        for row in self.ship_grid.grid:
            for node in row:
                grid.append((node.type, node.get_stats()))
        dump['GRID'] = grid
        # components
        component_list = []
        for component in self.component_inventory:
            if self.component_inventory.index(component) != 0:
                component_list.append(component.component_dict())
        dump["C_INV"] = component_list
        dump["C_ACT"] = self.installed_components
        # crew
        crew_list = []
        for crew in self.crew:
            crew_list.append(crew.get_data())
        dump["CREW"] = crew_list
        with open(file_name, 'w') as outfile:
            json.dump(dump, outfile)
        print('saved to file')


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

        self.preview_window = ShipPreview(self, (20, 490), (200, 200), zoom=4, padding=20)

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
                            s = self.selected_cell_stats
                            node.set_stats(s[0], s[1], s[2], s[3])
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


class ShipStats(object):
    def __init__(self, ship, font, small_font):
        self.ship = ship
        self.font = font
        self.small_font = small_font

    def draw(self, screen):
        self.ship.draw_ship(screen, position=(600, 100), color=Color.gray, zoom=10)
        Text.draw_text(screen, font=self.font, text='Teest test test', color=Color.green, position=(50, 50))
        y_offset = 0
        for stat, value in self.ship.ship_stats.items():
            formatted_stat = stat.capitalize()
            formatted_stat = formatted_stat.replace('_', ' ')
            Text.draw_text(screen, font=self.font, text='{0}: {1}'.format(formatted_stat, value), color=Color.white,
                           position=(40, 100+y_offset))
            y_offset += 30


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
        for skill, value in self.pawn.ship_skills.items():
            Text.draw_text(screen, self.small_font, '{0}:'.format(skill), Color.white, (25, y))
            Text.draw_text(screen, self.small_font, str(value), Color.white, (125, y))
            y += 30
        Text.draw_text(screen, self.font, 'STATS', Color.white, (175, 300))
        y = 350
        for stat, value in self.pawn.battle_skills.items():
            Text.draw_text(screen, self.small_font, '{0}:'.format(stat), Color.white, (175, y))
            Text.draw_text(screen, self.small_font, str(value), Color.white, (300, y))
            y += 30

    def update(self, key, mouse, offset=(0, 0)):
        pass
