"""Contains the main XML editor app class.

This package contains the main XML editor app class, which is used to direct all of the app's functions as well as
handling the GUI via helper classes and methods.
"""
from xml_editor.xml_editor import XmlEditor


def main() -> None:
    """Run the app inside a development environment.

    :return: None.
    """
    app = XmlEditor()
    app.mainloop()
