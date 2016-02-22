import json
import os
import pygame


class Event(object):
    def __init__(self, picture, text):
        self.data = None
        self.picture = picture
        self.text = text

    def read_event_file(self, event_file):
        try:
            with open(event_file) as data_file:
                self.data = json.load(data_file)
        except Exception as e:
            print 'Exception loading {0}: {1}'.format(event_file, e)

    def run_event(self, event_name):
        event = self.data[event_name]
        if event:
            if 'IMAGE' in event:
                self.picture.image = pygame.image.load(os.path.normpath(event['IMAGE']))
            if 'TEXT' in event:
                self.text.add_message('>> {0}'.format(event['TEXT']))
            if 'PAUSE' in event:
                print 'This wuld be a paws'
            if 'NEXT' in event:
                self.run_event(event['NEXT'])
