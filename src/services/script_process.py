"""Contains a process class for executing scripts in a background process."""
from __future__ import annotations

import multiprocessing as mp
from typing import TYPE_CHECKING

from enums.err_no_enum import ErrNoEnum
from errors.app_error import AppError
from factories.script_factory import ScriptFactory
from scripts.kocman import Kocman  # noqa: F401
from scripts.remove_ampersand import RemoveAmpersand  # noqa: F401

if TYPE_CHECKING:
    from pathlib import Path

    from scripts.script_base import ScriptBase
    from utils.queue_message import QueueMessage


class ScriptProcess(mp.Process):
    """Worker process responsible for executing a script in a background process."""

    def __init__(
            self,
            script_key: str,
            input_file: Path,
            output_folder: Path,
            inbound_queue: mp.Queue[QueueMessage],
            outbound_queue: mp.Queue[QueueMessage | AppError],
    ) -> None:
        """Initialise the worker process with only picklable attributes.

        :param script_key: Key under which the script is registered in the repository.
        :param input_file: Path to the input file to be processed.
        :param output_folder: Path to the output folder to save the processed file.
        :param inbound_queue: Queue used for messages sent to the script from GUI.
        :param outbound_queue: Queue used for messages sent from the script to GUI.
        :return: None.
        """
        super().__init__()
        self._script_key: str = script_key
        self._input_file: Path = input_file
        self._output_folder: Path = output_folder
        self._inbound_queue: mp.Queue[QueueMessage] = inbound_queue
        self._outbound_queue: mp.Queue[QueueMessage | AppError] = outbound_queue

    def run(self) -> None:
        """Run the script inside the child process.

        :return: None.
        """
        try:
            script: ScriptBase = ScriptFactory.create(
                key=self._script_key,
                input_file=self._input_file,
                output_folder=self._output_folder,
                outbound_queue=self._outbound_queue,
                inbound_queue=self._inbound_queue,
            )
            script.run()
        except AppError as e:
            self._outbound_queue.put(e)
        except Exception as e:
            self._outbound_queue.put(
                AppError(
                    error_message=f"Chyba při provádění skriptu: {e}",
                    error_code=ErrNoEnum.ERROR_REMOVING_XML_ELEMENTS,
                ),
            )
