import json
import os
import pygame


class Event(object):
    def __init__(self, panel, picture, text):
        self.data = None
        self.panel = panel
        self.picture = picture
        self.text = text

    def read_event_file(self, event_file):
        try:
            with open(event_file) as data_file:
                self.data = json.load(data_file)
        except Exception as e:
            print('Exception loading {0}: {1}'.format(event_file, e))

    def run_event(self, event_name):
        event = self.data[event_name]
        if event:
            if 'BATTLE' in event:
                pass
            if 'IMAGE' in event:
                self.picture.image = pygame.image.load(os.path.normpath(event['IMAGE']))
            if 'TEXT' in event:
                self.text.add_message('>> {0}'.format(event['TEXT']))
            if 'GOTO' in event:
                self.panel.switch_window(event['GOTO'])
            if 'PAUSE' in event:
                print('This wuld be a paws')
            if 'NEXT' in event:
                self.run_event(event['NEXT'])

    def adhoc_event(self, picture=None, text=None, goto=None, battle=None):
        if picture:
            self.picture.image = picture
        if text:
            self.text.add_message('>> {0}'.format(text))
        if goto:
            self.panel.switch_window(goto)
        if battle:
            self.panel.start_space_battle(battle)
