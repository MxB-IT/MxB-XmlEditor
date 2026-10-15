"""Contains a class used to instantiate and represent all frames within the app."""
from customtkinter import CTkFrame

from enums.colour_enum import ColourEnum


class FrameBase(CTkFrame):
    """Class used to instantiate and represent all frames within the app."""

    def __init__(
            self,
            *args,
            master,
            fg_color: ColourEnum = ColourEnum.WHITE,
            border_color: ColourEnum = ColourEnum.MXB_RED,
            border_width: int = 3,
            **kwargs,
        ) -> None:
        """Initialise the FrameBase class.

        Sets up all the provided attributes for its superclass or the preset default fallbacks.
        :param args: Positional arguments to pass to the superclass.
        :param master: Master widget used to wrap the frame.
        :param fg_color: Colour that the frame shall have.
        :param border_color: Border colour for the frame.
        :param border_width: Border width of the frame.
        :param kwargs: Keyword arguments to pass to the superclass.
        :return: None.
        """
        super().__init__(
            *args,
            master,
            fg_color = fg_color,
            border_color = border_color,
            border_width = border_width,
            **kwargs,
        )
