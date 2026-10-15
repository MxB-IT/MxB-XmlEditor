"""Contains an enumeration with all the error codes ever raised by the application."""
from enum import IntEnum


class ErrNoEnum(IntEnum):
    """Contains an enumeration with all the error codes ever needed by the application."""

    ERROR_REMOVING_XML_ELEMENTS = 101
    ERROR_WRITING_RESULT = 201
    PAYLOAD_IN_QUEUE_IS_NONE = 301
    UNKNOWN_QUEUE_STATUS = 302
