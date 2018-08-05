import pygame

import src.const.Color as Color
import settings
from src.Range import Range
from src.Ship import Ship
from src.components.text.TextBox import TextBox


class SpaceBattle(object):
    def __init__(self, player_ship, font, small_font, window_size, enemies=None):
        self.player_ship = player_ship
        self.font = font
        self.small_font = small_font
        self.window_size = window_size
        self.center = (self.window_size[0]/2, self.window_size[1]/2)

        if player_ship is None:
            print("You have no ship and you lose somehow")

        self.melee_range = Range(distance=100, center=self.center, ring_color=Color.RED)
        self.close_range = Range(distance=150, center=self.center, ring_color=Color.GRAY)
        self.far_range = Range(distance=200, center=self.center, ring_color=Color.D_GRAY)
        self.scanner_range = Range(distance=250, center=self.center, ring_color=Color.BLACK, ship_color=Color.D_GRAY)

        self.ranges = [self.melee_range, self.close_range, self.far_range, self.scanner_range]

        self.enemy_ships = []

        if enemies:
            for enemy in enemies:
                en_ship = Ship(size_x=40, size_y=40)
                en_ship.load("{0}{1}".format(settings.main_path, enemy["ship_file"]))
                self.scanner_range.enemies.append(en_ship)
                self.enemy_ships.append(en_ship)

        for ship in self.enemy_ships:
            print('attack: {0} - armor: {1} - speed: {2} - shield: {3}'.format(ship.ship_stats['attack'],
                                                                               ship.ship_stats['armor'],
                                                                               ship.ship_stats['speed'],
                                                                               ship.ship_stats["shield"]))

        self.side_panel = SpaceBattlePanel(self)

        self.target = None
        self.battle_state = {'move': 1,
                             'decide': 2}

    def update(self, key, mouse, offset=(0, 0)):
        for enemy in self.enemy_ships:
            if enemy.box.update(key=key, mouse=mouse, offset=offset):
                self.target = enemy
                print('hey got a target')
        # check movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            print('up')
        if keys[pygame.K_a]:
            print('left')
        elif keys[pygame.K_d]:
            print('right')

    def draw(self, screen):
        zoom = 4
        screen.fill(Color.BLACK)
        # center screen: player
        player_position = (self.center[0] - self.player_ship.get_ship_size(zoom=zoom)[0]/2,
                           self.center[1] - self.player_ship.get_ship_size(zoom=zoom)[1]/2)
        player = pygame.Surface(self.player_ship.get_ship_size(zoom=zoom))
        # player.fill(Color.black)
        self.player_ship.draw_ship(player, position=(0, 0), zoom=zoom)
        screen.blit(player, player_position)
        if self.player_ship.ship_stats['shield'] is not 0 and self.player_ship.current_shield > 0:
            shield_green = int(float(self.player_ship.current_shield) / float(self.player_ship.ship_stats['shield']) * 255)
            shield_red = 255 - shield_green
        else:
            shield_green = 0
            shield_red = 0
        pygame.draw.circle(screen, (shield_red, shield_green, 0), (int(self.center[0]), int(self.center[1])), 50, 10)
        # self.player_ship.draw_ship(screen, position=player_position, zoom=zoom)

        for circle in self.ranges:
            circle.draw(screen, self.target, zoom=zoom)
        # screen.blit(self.player_ship_sprite, (300, 400))
        # self.player_ship.draw_ship(screen, position=(300, 400), zoom=zoom)


class SpaceBattlePanel(object):
    def __init__(self, battle):
        self.battle = battle

        self.attack_but = TextBox(pygame.Rect(20, 50, 100, 40), box_color=Color.D_GRAY, border_color=Color.GRAY,
                                  highlight_color=Color.WHITE, active_color=Color.GRAY, name='Attack Button',
                                  message='ATTACK', text_color=Color.RED, text_outline=True, font=self.battle.font)
        self.defend_but = TextBox(pygame.Rect(20, 100, 100, 40), box_color=Color.D_GRAY, border_color=Color.GRAY,
                                  highlight_color=Color.WHITE, active_color=Color.GRAY, name='Defend Button',
                                  message='DEFEND', text_color=Color.BLUE, text_outline=True, font=self.battle.font)

    def update(self, key, mouse, offset=(0, 0)):
        if self.attack_but.update(key=key, mouse=mouse, offset=offset):
            if self.battle.target is None:
                print('You need a fuckin target mate')
            else:
                print('Gonna attack {0} then'.format(self.battle.target))
                # attack stuff
                self.battle.target = None

    def draw(self, screen):
        self.attack_but.draw(screen)
        self.defend_but.draw(screen)
