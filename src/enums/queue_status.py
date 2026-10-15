"""Contains an enum with all the multiprocessing queue statuses to be used in messages."""
from enum import StrEnum


class QueueStatus(StrEnum):
    """Contains all the multiprocessing queue statuses."""

    FINISHED = "FINISHED"
    INTERRUPT = "INTERRUPT"
    PROGRESS = "PROGRESS"
