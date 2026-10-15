"""Contains an enum containing all XML element tags to be detected by the app."""
from enum import StrEnum


class ElementTag(StrEnum):
    """Contains all the XML element tags to be detected by the app."""

    INVOICE_CREATED = "FaktVyd"
    ACCOUNT = "Ucet"
    TAX_CODE = "KodDPH"
    STORAGE_ITEM = "SklPolozka"
    CENTER = "Stredisko"
