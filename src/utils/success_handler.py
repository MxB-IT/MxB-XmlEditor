"""Contains a class used to display a window, informing the user about the success of the processing."""
from tkinter import BOTH
from typing import Any

from customtkinter import CTkToplevel

from widgets.button_base import ButtonBase
from widgets.frame_base import FrameBase
from widgets.label_base import LabelBase


class SuccessHandler(CTkToplevel):
    """Class used to create a pop-up window to inform the user about processing success."""

    def __init__(
            self,
            invoice_amt: int,
    ) -> None:
        """Initialise the SuccessHandler class, setting up all needed widgets and initialising the superclass.

        :param invoice_amt: Amount of invoices processed.
        :return: None.
        """
        super().__init__()
        self.title(
            "Úspěch",
        )

        self.__frame: FrameBase = FrameBase(
            master=self,
        )
        """Frame used to wrap all of the widgets inside the success pop-up window."""

        self.__frame.pack(
            fill=BOTH,
            expand=1,
        )

        self.__widgets: list[Any] = []
        """List of all widgets present in the success pop-up window."""

        self.__label: LabelBase = LabelBase(
            master=self.__frame,
            text=f"XML soubor úspěšně zpracován\n"
                 f"Upraveno bylo celkem {invoice_amt} faktur):",
        )
        """Label with information about the successful processing."""

        self.__widgets.append(
            self.__label,
        )

        self.__button: ButtonBase = ButtonBase(
            master=self.__frame,
            command=self.destroy,
            text="OK",
        )
        """Button used to close the pop-up window."""

        self.__widgets.append(
            self.__button,
        )

        for widget in self.__widgets:
            widget.pack(
                padx=5,
                pady=5,
                fill=BOTH,
                expand=1,
            )
