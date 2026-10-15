"""Contains a class used to process mangled XML files containing ampersands and correct them."""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from enums.err_no_enum import ErrNoEnum
from enums.file_type import FileType
from enums.queue_status import QueueStatus
from errors.app_error import AppError
from scripts.script_base import ScriptBase, get_step_size
from utils.queue_message import QueueMessage

if TYPE_CHECKING:
    import multiprocessing as mp
    from io import TextIOWrapper


class RemoveAmpersand(ScriptBase, key="RemoveAmpersand", display_name="Evropa Services Czech"):
    """Contains all the methods needed to correct mangled XML files containing ampersands."""

    def __init__(
            self,
            input_file: Path,
            output_folder: Path,
            outbound_queue: mp.Queue[QueueMessage | AppError],
            inbound_queue: mp.Queue[QueueMessage],
    ) -> None:
        """Initialise the RemoveAmpersand class.

        Initialises the RemoveAmpersand class with the provided arguments, passing what needs to be passed to the
        superclass.
        :param input_file: Mangled XML file to be processed.
        :param output_folder: Folder into which to save the output.
        :param outbound_queue: Multiprocessing queue used to send messages to the GUI.
        :param inbound_queue: Multiprocessing queue used to receive messages from the GUI.
        :return: None.
        """
        super().__init__(
            input_file=input_file,
            output_folder=output_folder,
            outbound_queue=outbound_queue,
            inbound_queue=inbound_queue,
        )

        file: TextIOWrapper = input_file.open(
            mode="r",
            encoding="utf-8",
        )
        lines: list[str] = list(file)
        self.__file_data: list[str] = list(lines)
        file.close()

    def run(self) -> None:
        """Run the script, processing the input.

        Fixes the mangled XML file, removing all the ampersands within, that are breaking it.
        :return: None.
        """
        invoice_counter: int = 0

        total_rows: int = len(self.__file_data)
        step: int = get_step_size(total_rows)

        text: str = "".join(self.__file_data)

        lines: list[str] = text.splitlines(
            keepends=True,
        )

        ctr: int = 0

        for i, line in enumerate(lines):
            ctr += 1

            if '<inv:invoice version="2.0">' in line:
                invoice_counter += 1

            if "&" in line:
                lines[i] = line.replace("&", "+")

            if ctr % step == 0:
                self._send_progress_message(
                    progress=ctr / total_rows,
                )

        text = "".join(lines)

        try:
            self._file_writer.write_file(
                path=Path(self._output_folder / f"Evropa services Czech-FV-{datetime.now(tz=UTC).strftime("%m-%Y")}.xml"),
                data=text,
                file_type=FileType.TEXT,
            )
        except Exception:
            self._send_message(
                message=AppError(
                    error_message=f"Chyba při zapisování souboru, zkontrolujte prosím, že nemáte otevřený soubor s"
                                  f"názvem Evropa services Czech-FV-{datetime.now(tz=UTC).strftime("%m-%Y")}.xml ve"
                                  f"složce {self._output_folder.name}.",
                    error_code=ErrNoEnum.ERROR_WRITING_RESULT,
                ),
            )

        self._send_message(
            QueueMessage(
                status=QueueStatus.FINISHED,
                payload=invoice_counter,
            ),
        )
