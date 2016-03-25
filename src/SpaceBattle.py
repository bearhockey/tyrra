import pygame

import Color
import settings

from Range import Range
from Ship import Ship
from TextBox import TextBox


class SpaceBattle(object):
    def __init__(self, player_ship, font, small_font, window_size):
        self.player_ship = player_ship
        self.font = font
        self.small_font = small_font
        self.window_size = window_size
        self.center = (self.window_size[0]/2, self.window_size[1]/2)

        if player_ship is None:
            print "You have no ship and you lose somehow"

        self.melee_range = Range(distance=100, center=self.center, ring_color=Color.red)
        self.close_range = Range(distance=150, center=self.center, ring_color=Color.gray)
        self.far_range = Range(distance=200, center=self.center, ring_color=Color.d_gray)
        self.scanner_range = Range(distance=250, center=self.center, ring_color=Color.black, ship_color=Color.d_gray)

        self.ranges = [self.melee_range, self.close_range, self.far_range, self.scanner_range]

        self.enemy_ships = []

        for _ in range(3):
            en_ship = Ship(size_x=40, size_y=40)
            en_ship.load('{0}data/enemy_1.txt'.format(settings.main_path))
            self.scanner_range.enemies.append(en_ship)
            # random.choice(self.ranges).enemies.append(en_ship)
            self.enemy_ships.append(en_ship)

        for ship in self.enemy_ships:
            print 'attack: {0} - armor: {1} - speed: {2}'.format(ship.attack_value.message,
                                                                 ship.armor_value.message,
                                                                 ship.speed_value.message)

        self.side_panel = SpaceBattlePanel(self)

        self.target = None
        self.battle_state = {'move': 1,
                             'decide': 2}

    def update(self, key, mouse, offset=(0, 0)):
        for enemy in self.enemy_ships:
            if enemy.box.update(key=key, mouse=mouse, offset=offset):
                self.target = enemy
                print 'hey got a target'
        # check movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            print 'up'
        if keys[pygame.K_a]:
            print 'left'
        elif keys[pygame.K_d]:
            print 'right'

    def draw(self, screen):
        zoom = 4
        screen.fill(Color.black)
        # center screen: player
        player_position = (self.center[0] - self.player_ship.get_ship_size(zoom=zoom)[0]/2,
                           self.center[1] - self.player_ship.get_ship_size(zoom=zoom)[1]/2)
        player = pygame.Surface(self.player_ship.get_ship_size(zoom=zoom))
        player.fill(Color.black)
        self.player_ship.draw_ship(player, position=(0, 0), zoom=zoom)
        screen.blit(player, player_position)
        # self.player_ship.draw_ship(screen, position=player_position, zoom=zoom)

        for circle in self.ranges:
            circle.draw(screen, self.target, zoom=zoom)
        # screen.blit(self.player_ship_sprite, (300, 400))
        # self.player_ship.draw_ship(screen, position=(300, 400), zoom=zoom)


class SpaceBattlePanel(object):
    def __init__(self, battle):
        self.battle = battle

        self.attack_but = TextBox(pygame.Rect(20, 50, 100, 40), box_color=Color.d_gray, border_color=Color.gray,
                                  highlight_color=Color.white, active_color=Color.gray, name='Attack Button',
                                  message='ATTACK', text_color=Color.red, text_outline=True, font=self.battle.font)
        self.defend_but = TextBox(pygame.Rect(20, 100, 100, 40), box_color=Color.d_gray, border_color=Color.gray,
                                  highlight_color=Color.white, active_color=Color.gray, name='Defend Button',
                                  message='DEFEND', text_color=Color.blue, text_outline=True, font=self.battle.font)

    def update(self, key, mouse, offset=(0, 0)):
        if self.attack_but.update(key=key, mouse=mouse, offset=offset):
            if self.battle.target is None:
                print 'You need a fuckin target mate'
            else:
                print 'Gonna attack {0} then'.format(self.battle.target)
                # attack stuff
                self.battle.target = None

    def draw(self, screen):
        self.attack_but.draw(screen)
        self.defend_but.draw(screen)
