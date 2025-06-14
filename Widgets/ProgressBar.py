from Widgets.WidgetsBase import *

class ProgressBarBase(CTkProgressBar):
    def __init__(self,
                 *args,
                 fg_color=MXB_RED,
                 progress_color="white",
                 **kwargs):
        super().__init__(*args,
                         fg_color=fg_color,
                         progress_color=progress_color,
                         **kwargs)