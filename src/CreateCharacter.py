import os

import pygame

import Color
import settings
from Pawn import Pawn
from src.components.text import Text
from src.components.Box import Box
from src.components.text.InputBox import InputBox
from src.components.text.TextBox import TextBox


class CreateCharacter(object):
    def __init__(self, big_font, font, small_font, screen_height=800, screen_width=600):
        self.big_font = big_font
        self.font = font
        self.small_font = small_font
        self.box = Box(pygame.Rect(int(screen_width * 0.1), int(screen_height * 0.1),
                                   int(screen_width * 0.8), int(screen_height * 0.8)),
                       box_color=Color.black, border_color=Color.white, border=4, highlight_box=False,
                       name='Character Creation Box')
        box_x = self.box.rect.x
        box_y = self.box.rect.y
        # build portrait roster
        self.portrait_roster = []
        self.portrait_index = 0
        for face in os.listdir(settings.face_path):
            if face.endswith('.png'):
                path = os.path.join(settings.face_path, face)
                self.portrait_roster.append({"PATH": path, "IMAGE": pygame.image.load(path)})
        for face in os.listdir(settings.mod_path):
            if face.endswith('.png'):
                path = os.path.join(settings.mod_path, face)
                self.portrait_roster.append({"PATH": path, "IMAGE": pygame.image.load(path)})

        self.portrait = None
        self.portrait_box = Box(pygame.Rect(int(box_x + self.box.rect.width / 10),
                                            int(box_y + self.box.rect.height / 7),
                                            250, 250),
                                box_color=Color.black, border_color=Color.white, highlight_box=False,
                                name='Portrait Box')
        self.update_roster_portrait_box()
        self.left_portrait = TextBox(pygame.Rect(self.portrait_box.rect.x - 35,
                                                 self.portrait_box.rect.y + self.portrait_box.rect.height/3,
                                                 25, 40),
                                     box_color=Color.d_gray, border_color=Color.white, highlight_color=Color.gray,
                                     active_color=Color.white, name='p_left', message='<', text_color=Color.white,
                                     text_outline=True, font=self.font)
        self.right_portrait = TextBox(pygame.Rect(self.portrait_box.rect.x + self.portrait_box.rect.width + 10,
                                                  self.portrait_box.rect.y + self.portrait_box.rect.height/3,
                                                  25, 40),
                                      box_color=Color.d_gray, border_color=Color.white, highlight_color=Color.gray,
                                      active_color=Color.white, name='p_right', message='>', text_color=Color.white,
                                      text_outline=True, font=self.font)
        # character name
        self.name = InputBox(pygame.Rect(box_x + self.box.rect.width / 2.4, box_y + self.box.rect.height/7, 400, 35),
                             box_color=Color.d_gray, border_color=Color.gray, highlight_color=Color.white,
                             active_color=Color.blue, message='Flash', text_color=Color.white, font=self.font,
                             text_limit=32)
        # character age
        self.age = InputBox(pygame.Rect(box_x + self.box.rect.width / 2.4, box_y + self.box.rect.height/2.7, 70, 35),
                            box_color=Color.d_gray, border_color=Color.gray, highlight_color=Color.white,
                            active_color=Color.blue, message='25', text_color=Color.white, font=self.font,
                            text_limit=5, allowed_characters=range(48, 58))
        # character race
        self.race = InputBox(pygame.Rect(box_x + self.box.rect.width / 2.4, box_y + self.box.rect.height/4, 400, 35),
                             box_color=Color.d_gray, border_color=Color.gray, highlight_color=Color.white,
                             active_color=Color.blue, message='Human', text_color=Color.white, font=self.font,
                             text_limit=32)
        # character bio
        self.bio = InputBox(pygame.Rect(box_x + self.box.rect.width / 2.4, box_y + self.box.rect.height/2, 400, 50),
                            box_color=Color.d_gray, border_color=Color.gray, highlight_color=Color.white,
                            active_color=Color.blue, message='A little bit about myself', text_color=Color.white,
                            font=self.font, text_limit=300)
        # profession stuff
        self.profession_list = ['Pilot', 'Guns', 'Engineer', 'Medic', 'Scientist']
        self.profession = TextBox(pygame.Rect(self.portrait_box.rect.x + self.portrait_box.rect.width/2,
                                              self.portrait_box.rect.y + self.portrait_box.rect.width + 20,
                                              100, 20),
                                  highlight_color=Color.white, active_color=Color.gray, border=0, name='Profession',
                                  message=self.profession_list[0], text_color=Color.gray, font=self.small_font,
                                  highlight_box=False, highlight_text=True)

        self.skills = {}
        self.update_profession_stats()
        # done
        self.done = TextBox(pygame.Rect(box_x + self.box.rect.width - 150, box_y + self.box.rect.height - 100, 100, 50),
                            box_color=Color.red, border_color=Color.gray, highlight_color=Color.white,
                            active_color=Color.gray, name='done', message='START', text_color=Color.white,
                            text_outline=True, font=self.font)

    def return_character(self):
        pawn = Pawn(name=self.name.message, age=self.age.message, race=self.race.message, bio=self.bio.message,
                    profile=self.portrait_roster[self.portrait_index]["PATH"], battle_skills=self.skills)
        pawn.ship_skills[self.profession.message] = 1
        return pawn

    def update_roster_portrait_box(self):
        self.portrait = self.portrait_roster[self.portrait_index]["IMAGE"]
        self.portrait_box.image = self.portrait

    def update_profession_stats(self):
        if self.profession.message == 'Pilot':
            self.skills = {'Melee': 2, 'Ranged': 1, 'Defense': 1, 'Intelligence': 1, 'Speed': 1}
        elif self.profession.message == 'Guns':
            self.skills = {'Melee': 1, 'Ranged': 2, 'Defense': 1, 'Intelligence': 1, 'Speed': 1}
        elif self.profession.message == 'Engineer':
            self.skills = {'Melee': 1, 'Ranged': 1, 'Defense': 1, 'Intelligence': 1, 'Speed': 2}
        elif self.profession.message == 'Medic':
            self.skills = {'Melee': 1, 'Ranged': 1, 'Defense': 2, 'Intelligence': 1, 'Speed': 1}
        elif self.profession.message == 'Scientist':
            self.skills = {'Melee': 1, 'Ranged': 1, 'Defense': 1, 'Intelligence': 2, 'Speed': 1}

    def update(self, key, mouse, offset=(0, 0)):
        if self.portrait_index > 0 and self.left_portrait.update(key=key, mouse=mouse, offset=offset):
            self.portrait_index -= 1
            self.update_roster_portrait_box()
        if self.portrait_index < len(self.portrait_roster)-1 \
                and self.right_portrait.update(key=key, mouse=mouse, offset=offset):
            self.portrait_index += 1
            self.update_roster_portrait_box()
        self.name.update(key=key, mouse=mouse, offset=offset)
        self.age.update(key=key, mouse=mouse, offset=offset)
        self.race.update(key=key, mouse=mouse, offset=offset)
        self.bio.update(key=key, mouse=mouse, offset=offset)
        #
        if self.profession.update(key=key, mouse=mouse, offset=offset):
            if self.profession.message == self.profession_list[-1]:
                self.profession.message = self.profession_list[0]
            else:
                self.profession.message = self.profession_list[self.profession_list.index(self.profession.message)+1]
            self.update_profession_stats()
        #
        if self.done.update(key=key, mouse=mouse, offset=offset):
            return self.return_character()
        return

    def draw(self, screen):
        self.box.draw(screen)
        # non-interactive
        title = 'Create Your Character'
        title_width = self.big_font.size(title)[0]
        Text.draw_text(screen, self.big_font, text=title, color=Color.blue,
                       position=(self.box.rect.x+(self.box.rect.width - title_width)/2, self.box.rect.y + 5))

        Text.draw_text(screen, self.small_font, text='Name:', color=Color.green,
                       position=(self.name.rect.x, self.name.rect.y - 20))
        Text.draw_text(screen, self.small_font, text='Race:', color=Color.green,
                       position=(self.race.rect.x, self.race.rect.y - 20))
        Text.draw_text(screen, self.small_font, text='Age:', color=Color.green,
                       position=(self.age.rect.x, self.age.rect.y - 20))
        Text.draw_text(screen, self.small_font, text='Biography:', color=Color.green,
                       position=(self.bio.rect.x, self.bio.rect.y - 20))

        # profession box
        Text.draw_text(screen, self.small_font, text='Profession:', color=Color.l_gray,
                       position=(self.portrait_box.rect.x, self.profession.rect.y))
        # stats
        i = 25
        for key, value in self.skills.iteritems():
            Text.draw_text(screen, self.small_font, text=key, color=Color.l_gray,
                           position=(self.portrait_box.rect.x, self.profession.rect.y + i))
            Text.draw_text(screen, self.small_font, text=value, color=Color.l_gray,
                           position=(self.portrait_box.rect.x + self.portrait_box.rect.width/2,
                                     self.profession.rect.y + i))
            i += 25

        # buttons and things
        self.portrait_box.draw(screen)
        self.left_portrait.draw(screen)
        self.right_portrait.draw(screen)
        # boxes
        self.name.draw(screen)
        self.race.draw(screen)
        self.age.draw(screen)
        self.bio.draw(screen)
        #
        self.profession.draw(screen)
        #
        self.done.draw(screen)
