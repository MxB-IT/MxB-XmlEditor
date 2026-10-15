"""Contains a class used for displaying error windows to the user as needed during runtime."""
from tkinter import BOTH
from typing import Any

from customtkinter import CTkToplevel

from widgets.button_base import ButtonBase
from widgets.frame_base import FrameBase
from widgets.label_base import LabelBase


class ErrorHandler(CTkToplevel):
    """Class used to display error windows to the user as needed during runtime."""

    def __init__(
            self,
            *args,
            error_message: str,
            error_code: int,
            **kwargs
        ) -> None:
        """Initialise the ErrorHandler class, setting up the error code and message that should be displayed.

        :param args: Positional arguments to pass to the superclass.
        :param error_message: Error message to display to the user.
        :param error_code: Code of the error raised, to ascertain where the error originated for debugging.
        :param kwargs: Keyword arguments to pass to the superclass.
        :return: None.
        """
        super().__init__(*args,
                         **kwargs)
        self.title(
            "ERROR",
        )

        self.__frame: FrameBase = FrameBase(
            master=self,
        )
        """Frame used to wrap all the widgets inside the pop-up window."""

        self.__frame.pack(
            fill=BOTH,
            expand=1,
        )

        self.__widgets: list[Any] = []
        """List of all the widgets within the error pop-up window."""

        self.__error_message = LabelBase(
            master=self.__frame,
            text=f"ERROR {error_code}: {error_message}",
        )
        """Label used to display the message raised coinciding with the raised error."""

        self.__widgets.append(
            self.__error_message,
        )

        self.__done_button=ButtonBase(
            master=self.__frame,
            text="OK",
            command=self.destroy,
        )
        """Button used to close the pop-up success window."""

        self.__widgets.append(
            self.__done_button,
        )

        for widget in self.__widgets:
            widget.pack(
                padx=5,
                pady=5,
                fill=BOTH,
                expand=1,
            )
