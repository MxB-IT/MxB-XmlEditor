from Widgets.LabelBase import *
from Widgets.ButtonBase import *
from Widgets.FrameBase import *
from Widgets.TextBoxBase import *

class SuccessHandler(CTkToplevel):
    def __init__(self, invoice_amt):
        super().__init__()
        self.title("Úspěch")
        self.frame = FrameBase(master=self)
        self.frame.pack(fill=BOTH, expand=1)
        self.widgets=list()
        self.label=LabelBase(master=self.frame,
                             text=f"XML soubor úspěšně zpracován\n"
                                  f"Upraveno bylo celkem {invoice_amt} faktur):")
        self.widgets.append(self.label)
        self.button=ButtonBase(master=self.frame,
                               command=self.destroy,
                               text="OK")
        self.widgets.append(self.button)

        for widget in self.widgets:
            widget.pack(padx=5,
                        pady=5,
                        fill=BOTH,
                        expand=1)