from Widgets.WidgetsBase import *


class TextBoxBase(CTkTextbox):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 text_color=MXB_RED,
                 **kwargs):
        super().__init__(*args,
                         master=master,
                         text_color=text_color,
                         **kwargs)