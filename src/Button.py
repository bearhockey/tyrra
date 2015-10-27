from TextBox import TextBox


class Button(TextBox):
    def __init__(self, rect, box_color=None, border_color=None, message='', text_color=None, font=None):
        TextBox.__init__(self, rect, box_color, border_color, message, text_color, font)

    def check_click(self):
        if TextBox.check_click(self):
            return True
        else:
            return False
