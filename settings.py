import os
import re

global main_path
global src_path
global res_path
global face_path
global data_path
global mod_path


def init():
    global main_path
    global src_path
    global res_path
    global face_path
    global data_path
    global mod_path
    script = os.path.abspath(os.path.realpath(__file__))
    main_path = re.sub('settings\.pyc?', '', script)
    src_path = os.path.join(main_path, 'src')
    res_path = os.path.join(main_path, 'res')
    face_path = os.path.join(res_path, 'face')
    data_path = os.path.join(main_path, 'data')
    mod_path = os.path.join(main_path, 'mod')
