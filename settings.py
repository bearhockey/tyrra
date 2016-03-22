import os
import re

global main_path


def init():
    global main_path
    script = os.path.abspath(os.path.realpath(__file__))
    main_path = re.sub('settings\.pyc?', '', script)
    print 'Running out of {0}'.format(main_path)
