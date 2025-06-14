from Widgets.WidgetsBase import *

class ButtonBase(CTkButton):
    def __init__(self,
                 *args,
                 fg_color=DARK_MXB_RED,
                 **kwargs):
        super().__init__(*args,
                         fg_color=fg_color,
                         **kwargs)