"""Contains a class used to instantiate and represent all buttons within the app."""
from customtkinter import CTkButton

from enums.colour_enum import ColourEnum


class ButtonBase(CTkButton):
    """Class used to instantiate and represent all buttons within the app."""

    def __init__(
            self,
            *args,
            fg_color: ColourEnum=ColourEnum.MXB_RED,
            hover_color: ColourEnum=ColourEnum.DARK_MXB_RED,
            **kwargs,
            ) -> None:
        """Initialise the Button with preset attributes if no overrides are provided.

        :param args: Positional arguments passed to the customtkinter button class.
        :param fg_color: Foreground colour of the button.
        :param hover_color: Hover colour of the button.
        :param kwargs: Keyword arguments passed to the customtkinter button class.
        """
        super().__init__(
            *args,
            fg_color=fg_color,
            hover_color=hover_color,
            **kwargs,
        )
