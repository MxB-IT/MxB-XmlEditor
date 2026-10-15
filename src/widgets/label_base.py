"""Contains a class used to instantiate and represent all labels within the app."""
from customtkinter import CTkFrame, CTkLabel

from enums.colour_enum import ColourEnum


class LabelBase(CTkLabel):
    """Class used to instantiate and represent all labels within the app."""

    def __init__(
            self,
            *args,
            master: CTkFrame,
            text_color: ColourEnum = ColourEnum.MXB_RED,
            **kwargs,
    ) -> None:
        """Initialise the LabelBase class.

        Sets up the LabelBase class, taking the passed arguments or their predefined fallbacks and passing them to the
        superclass.
        :param args: Positional arguments to pass to the superclass.
        :param master: Widget used to wrap the label.
        :param text_color: Colour of the text within the label.
        :param kwargs: Keyword arguments to pass to the superclass.
        :return: None.
        """
        super().__init__(
            *args,
            master=master,
            text_color = text_color,
            **kwargs,
        )
