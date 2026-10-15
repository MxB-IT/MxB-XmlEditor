"""Contains a class used to transmit messages through a multiprocessing queue."""
from typing import Any

from enums.queue_status import QueueStatus


class QueueMessage:
    """Class used to transmit messages through a multiprocessing queue.

    The class contains a status and additional payload if it is required.
    """

    def __init__(
            self,
            status: QueueStatus,
            payload: Any | None = None,
    ) -> None:
        """Initialise a new instance of QueueMessage.

        Initialise the QueueMessage, setting the status and payload.
        :param status: The status to be sent via the queue.
        :param payload: The payload to be sent via the queue, None by default.
        :return: None.
        """
        self.status: QueueStatus = status
        self.payload: Any | None = payload
