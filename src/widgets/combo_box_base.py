"""Contains a class serving as a base for all comboboxes within the app.

Contains the ComboBoxBase class, which is used to initialise every single combobox within the app.
"""
from customtkinter import CTkComboBox, CTkFrame

from enums.colour_enum import ColourEnum


class ComboBoxBase(CTkComboBox):
    """Serves as the base class for all comboboxes within the app, setting up base parameters when initialised."""

    def __init__(
        self,
        *args,
        master: CTkFrame,
        border_color: ColourEnum = ColourEnum.MXB_RED,
        fg_color: ColourEnum = ColourEnum.WHITE,
        dropdown_fg_color: ColourEnum = ColourEnum.WHITE,
        button_color: ColourEnum = ColourEnum.MXB_RED,
        text_color: ColourEnum = ColourEnum.DARKER_MXB_RED,
        dropdown_text_color: ColourEnum = ColourEnum.DARKER_MXB_RED,
        dropdown_hover_color: ColourEnum = ColourEnum.DARK_MXB_RED,
        border_width: int = 3,
        button_hover_color: ColourEnum = ColourEnum.DARK_MXB_RED,
        **kwargs
    ) -> None:
        """Initialise the ComboBoxBase class.

        Initialises the ComboBoxBase class, which is used to initialise every single combobox within the app to maintain
        the app's visual consistency.
        :param args: Positional arguments to be passed to the underlying Combobox class.
        :param master: Reference to the parent tkinter object used to wrap around this combobox.
        :param border_color: Border colour of the combobox.
        :param fg_color: Foreground colour of the combobox.
        :param dropdown_fg_color: Foreground colour of the dropdown element of the combobox.
        :param button_color: Colour of the button used to open the dropdown portion of the combobox.
        :param text_color: Colour used for the text contained in the combobox.
        :param dropdown_text_color: Colour used for the text contained in the dropdown element of the combobox.
        :param dropdown_hover_color: Colour used for the dropdown element of the combobox when hovered over.
        :param border_width: Border width of the combobox.
        :param button_hover_color: Hover colour of the button used to open the dropdown portion of the combobox.
        :param kwargs: Keyword arguments to be passed to the underlying customtkinter Combobox class.
        :return: None.
        """
        super().__init__(
            *args,
             master,
             border_color=border_color,
             fg_color=fg_color,
             dropdown_fg_color=dropdown_fg_color,
             button_color=button_color,
             text_color=text_color,
             dropdown_text_color=dropdown_text_color,
             border_width=border_width,
             dropdown_hover_color=dropdown_hover_color,
             button_hover_color=button_hover_color,
             **kwargs,
        )
