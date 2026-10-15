"""Contains an enum with all the required element texts to look for."""
from enum import StrEnum


class ElementText(StrEnum):
    """Contains all the element texts to look for within the XML."""

    CASH = "HOTOVĚ!"
    CASH_REPLACE = "POK"
    PP = "PP"
    PP_REPLACE = "BAN"
    ZDANPLN = "U-ZDANPLN"
    ZDANPLN_REPLACE = "19Ř01,02"

