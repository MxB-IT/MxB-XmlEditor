"""Contains an enum with all the filetypes the FileWriterService is able to write."""
from enum import StrEnum


class FileType(StrEnum):
    """Class containing an enumeration of filetypes that the app can output."""

    TEXT = "TEXT"
    XML = "XML"
