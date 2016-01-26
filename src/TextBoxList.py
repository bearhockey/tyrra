from TextBox import TextBox


class TextBoxList(object):
    def __init__(self, rect, box_color=None, border_color=None, highlight_color=None, active_color=None, border=2,
                 name=None, text_color=None, text_outline=True, font=None, list_size=5, line_size=25):
        # not making this a template of Box or TextBox because for some reason it won't initialize all the variables
        self.rect = rect
        self.box_color = box_color
        self.border_color = border_color
        self.highlight_color = highlight_color
        self.active_color = active_color
        self.border = border
        self.name = name
        self.text_color = text_color
        self.text_outline = text_outline
        self.font = font
        #
        self.list_size = list_size
        self.line_size = line_size
        if self.list_size < 1:
            self.list_size = 1
        self.text_boxes = []

    def add_message(self, message=''):
        print 'start append'
        print ''
        for text_box in self.text_boxes:
            text_box.rect.top += self.line_size
            print 'line size is {0}'.format(self.line_size)
            print 'top is {0} for ({1})'.format(text_box.rect.top, text_box.message)
        self.text_boxes.append(TextBox(self.rect, box_color=self.box_color, border_color=self.border_color,
                                       highlight_color=self.highlight_color, active_color=self.active_color,
                                       border=self.border, name=self.name, message=message, text_color=self.text_color,
                                       text_outline=self.text_outline, font=self.font))
        if len(self.text_boxes) > self.list_size:
            self.text_boxes.pop(0)

    def update(self, key, mouse, offset=(0, 0)):
        for box in self.text_boxes:
            return box.update(self, key, mouse, offset)

    def draw(self, screen):
        for box in self.text_boxes:
            box.draw(screen)
