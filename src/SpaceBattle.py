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

        en_ship = Ship(size_x=40, size_y=40)
        en_ship.load('../data/enemy_1.txt')

        self.enemy_ships.append(en_ship)

        for ship in self.enemy_ships:
            print 'attack: {0}'.format(ship.attack_value.message)

        self.side_panel = SpaceBattlePanel(self)

    def draw(self, screen):
        screen.fill(Color.black)
        for ship in self.enemy_ships:
            ship.ship_preview.draw(screen, position=(300, 50))
        self.player_ship.ship_preview.draw(screen, position=(300, 400))


class SpaceBattlePanel(object):
    def __init__(self, battle):
        self.battle = battle

        self.attack_but = TextBox(pygame.Rect(20, 50, 100, 40), box_color=Color.d_gray, border_color=Color.gray,
                                  highlight_color=Color.white, active_color=Color.gray, name='Attack Button',
                                  message='ATTACK', text_color=Color.red, text_outline=True, font=self.battle.font)
        self.defend_but = TextBox(pygame.Rect(20, 100, 100, 40), box_color=Color.d_gray, border_color=Color.gray,
                                  highlight_color=Color.white, active_color=Color.gray, name='Defend Button',
                                  message='DEFEND', text_color=Color.blue, text_outline=True, font=self.battle.font)

    def draw(self, screen):
        self.attack_but.draw(screen)
        self.defend_but.draw(screen)
