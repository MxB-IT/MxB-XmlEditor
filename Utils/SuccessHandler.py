from Widgets.LabelBase import *
from Widgets.ButtonBase import *
from Widgets.FrameBase import *
from Widgets.TextBoxBase import *

class SuccessHandler(CTkToplevel):
    def __init__(self, text_to_display):
        super().__init__()
        self.title("Úspěch")
        self.frame = FrameBase(master=self)
        self.frame.pack(fill=BOTH, expand=1)
        self.widgets=list()
        self.label=LabelBase(master=self.frame,
                             text=f"XML soubor úspěšně zpracován\n"
                                  f"Upraveny/odstraněny byly tyto řádky (celkem {len(text_to_display)}):")
        self.widgets.append(self.label)
        self.textbox = TextBoxBase(master=self.frame,
                                   text_color="white",
                                   wrap="none")
        self.widgets.append(self.textbox)
        for line in text_to_display:
            self.textbox.insert(index=END,
                                text=f"{line}\n")
        self.textbox.configure(state=DISABLED)
        self.button=ButtonBase(master=self.frame,
                               command=self.destroy,
                               text="OK")
        self.widgets.append(self.button)

        for widget in self.widgets:
            widget.pack(padx=5,
                        pady=5,
                        fill=BOTH,
                        expand=1)