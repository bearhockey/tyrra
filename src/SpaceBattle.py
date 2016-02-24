import pygame

import Color

from TextBox import TextBox
from Ship import Ship


class SpaceBattle(object):
    def __init__(self, player_ship, font, small_font):
        self.player_ship = player_ship
        self.font = font
        self.small_font = small_font

        if player_ship is None:
            print "You have no ship and you lose somehow"

        self.enemy_ships = []

        for _ in range(3):
            en_ship = Ship(size_x=40, size_y=40)
            en_ship.load('data/enemy_1.txt')
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
        enemy_start_x = 350 - len(self.enemy_ships)*50
        x_offset = 0
        for ship in self.enemy_ships:
            if ship == self.target:
                color = Color.red
            else:
                color = Color.white
            ship.draw_ship(screen, position=(enemy_start_x+x_offset, 50), color=color, zoom=zoom)
            x_offset += 100
        self.player_ship.draw_ship(screen, position=(300, 400), zoom=zoom)


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
