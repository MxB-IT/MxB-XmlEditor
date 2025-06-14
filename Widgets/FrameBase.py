from Widgets.WidgetsBase import *

class FrameBase(CTkFrame):
    def __init__(self,
                 *args,
                 master,
                 fg_color = "white",
                 border_color = MXB_RED,
                 border_width = 2,
                 **kwargs):
        super().__init__(*args,
                         master,
                         fg_color = fg_color,
                         border_color = border_color,
                         border_width = border_width,
                         **kwargs)