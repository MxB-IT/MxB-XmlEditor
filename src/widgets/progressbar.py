"""Contains a class used to instantiate and represent all progressbars within the app."""
from customtkinter import CTkProgressBar

from enums.colour_enum import ColourEnum


class ProgressBarBase(CTkProgressBar):
    """Class used to initialise and represent all the progressbars within the app."""

    def __init__(
            self,
            *args,
            fg_color: ColourEnum=ColourEnum.MXB_RED,
            progress_color: ColourEnum=ColourEnum.WHITE,
            **kwargs,
    ) -> None:
        """Initialise the ProgressBarBase class.

        Passes all the provided arguments to the superclass, using predefined fallback values if nothing's been passed.
        :param args: Positional arguments to pass to the superclass.
        :param fg_color: Colour of the progressbar's background.
        :param progress_color: Colour of the progressbar.
        :param kwargs: Keyword arguments to pass to the superclass.
        :return: None.
        """
        super().__init__(
            *args,
            fg_color=fg_color,
            progress_color=progress_color,
            **kwargs,
        )
