"""Contains a base class for all scripts, which handles multiprocessing communication."""
from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from enums.file_type import FileType
from enums.queue_status import QueueStatus
from services.file_writer_service.file_writer_service import FileWriterService
from services.file_writer_service.string_writer import StringWriter
from services.file_writer_service.xml_writer import XMLWriter
from utils.queue_message import QueueMessage

if TYPE_CHECKING:
    import multiprocessing as mp
    from pathlib import Path

    from errors.app_error import AppError


def get_step_size(
        total_elements: int,
) -> int:
    """Get the step size for progress messages.

    :param total_elements: Total number of elements to process.
    :return: Step size.
    """
    return max(1, total_elements // 100)


class ScriptBase(ABC):
    """Base class for all scripts, handles multiprocessing communication. Contains a registry of all subclasses."""

    registry: dict[str, type[ScriptBase]] = {}
    """Registry for all scripts that are subclasses of ScriptBase."""

    display_name: str = ""
    """Display name for the script to be shown in the GUI."""

    def __init_subclass__(
            cls,
            key: str,
            display_name: str,
            **kwargs: dict[str, Any],
    ) -> None:
        """Detect and initialise subclasses to the ScriptBase.

        :param key: Key under which the subclass shall exist within the repository.
        :param display_name: Display name of the script to be shown in the GUI.
        :param kwargs: Any other keyword arguments passed to the init method.
        """
        super().__init_subclass__(**kwargs)
        cls.display_name = display_name
        cls.registry[key] = cls

    def __init__(
            self,
            input_file: Path,
            output_folder: Path,
            outbound_queue: mp.Queue[QueueMessage | AppError],
            inbound_queue: mp.Queue[QueueMessage],
    ) -> None:
        """Initialise the ScriptBase.

        Inititalises the ScriptBase, setting up the inbound and outbound queues and storing references to the input file
        and output folder.
        :param input_file: Path to the input file to be processed.
        :param output_folder: Path to the output folder to save the processed file.
        :param outbound_queue: Multiprocessing queue used to send messages to the GUI.
        :param inbound_queue: Multiprocessing queue used to receive messages from the GUI.
        """
        self._input_file: Path = input_file
        """Contains a path to the input file on the user's drive."""

        self._output_folder: Path = output_folder
        """Contains a path to the output folder on the user's drive."""

        self.__outbound_queue: mp.Queue[QueueMessage | AppError] = outbound_queue
        """Queue for outbound messages sent to the GUI."""

        self.__inbound_queue: mp.Queue[QueueMessage] = inbound_queue
        """Queue for inbound messages coming from the GUI to the script."""

        self._stop_event: threading.Event = threading.Event()
        """Threading event used to stop the background procesing when the app is closed."""

        self._file_writer: FileWriterService = FileWriterService()
        """FileWriterService instance used to write output into files."""

        self._file_writer.register_writer(
            file_type=FileType.TEXT,
            writer=StringWriter(),
        )

        self._file_writer.register_writer(
            file_type=FileType.XML,
            writer=XMLWriter(),
        )

        __queue_listener: threading.Thread = threading.Thread(
            target=self.__queue_listener,
            daemon=True,
        )
        """Thread used to catch messages from the inbound queue and process them."""

        __queue_listener.start()

    def __queue_listener(self) -> None:
        """Listen to the inbound queue for any incoming messages and process them as they come.

        :return: None.
        """
        while True:
            msg: QueueMessage = self.__inbound_queue.get()
            if msg.status == QueueStatus.INTERRUPT:
                self._stop_event.set()
                break

    def _send_message(
            self,
            message: QueueMessage | AppError,
    ) -> None:
        """Send a message to the GUI via the outbound queue.

        Puts a message into the outbound queue for the GUI to catch and process.
        :param message: Message to be sent to the GUI.
        :return: None.
        """
        self.__outbound_queue.put(message)

    def _send_progress_message(
            self,
            progress: float,
    ) -> None:
        """Send a progress message to the GUI via the outbound queue.

        Puts a message into the outbound queue for the GUI to catch and process.
        :param progress: Progress to be sent to the GUI.
        :return: None.
        """
        self._send_message(
            message=QueueMessage(
                status=QueueStatus.PROGRESS,
                payload=progress,
            ),
        )

    @abstractmethod
    def run(self) -> None:
        """Run the underlying script."""
