"""Contains a class with all the methods and attributes needed to process Kocman files."""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import defusedxml.ElementTree as defusedET  # type: ignore[import-untyped]

from enums.element_tag import ElementTag
from enums.element_text import ElementText
from enums.err_no_enum import ErrNoEnum
from enums.file_type import FileType
from enums.queue_status import QueueStatus
from errors.app_error import AppError
from scripts.script_base import ScriptBase, get_step_size
from utils.queue_message import QueueMessage

if TYPE_CHECKING:
    import multiprocessing as mp
    import xml.etree.ElementTree as ET


class Kocman(ScriptBase, key="Kocman", display_name="Radomír Kocman"):
    """Contains all the methods and attributes needed to process Kocman files."""

    def __init__(
            self,
            input_file: Path,
            output_folder: Path,
            outbound_queue: mp.Queue[QueueMessage | AppError],
            inbound_queue: mp.Queue[QueueMessage],
    ) -> None:
        """Initialise the Kocman class.

        :param input_file: Path to the file to be processed by the script.
        :param output_folder: Path to the output folder to save the file into.
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

        self.__e_tree: ET.ElementTree[ET.Element[str] | None] = defusedET.parse(
            source=input_file,
        )

    def run(self) -> None:
        """Run the Kocman script, performing all the necessary operations.

        :return: None
        """
        invoice_counter: int = 0
        total_elements: int = len(list(self.__e_tree.iter()))
        ctr: int = 0
        step: int = get_step_size(total_elements)

        for element in self.__e_tree.iter():
            ctr += 1

            match element.tag:
                case ElementTag.INVOICE_CREATED:
                    invoice_counter += 1

                case ElementTag.ACCOUNT:
                    match element.text:
                        case ElementText.CASH:
                            element.text = ElementText.CASH_REPLACE

                        case ElementText.PP:
                            element.text = ElementText.PP_REPLACE

                        case _:
                            pass
                case ElementTag.TAX_CODE:
                    if element.text == ElementText.ZDANPLN:
                        element.text = ElementText.ZDANPLN_REPLACE

                case _:
                    pass

            for child in element:
                if child.tag in (ElementTag.STORAGE_ITEM, ElementTag.CENTER):
                    child.clear()
                    element.remove(child)
            if ctr % step == 0 or ctr == total_elements:
                self._send_progress_message(
                    progress=ctr / total_elements,
                )

        try:
            self._file_writer.write_file(
                path=Path(self._output_folder / f"Radomír Kocman-FV-{datetime.now(tz=UTC).strftime('%m-%Y')}.xml"),
                data=self.__e_tree,
                file_type=FileType.XML,
            )
        except Exception:
            self._send_message(
                message=AppError(
                    error_message=f"Chyba při zapisování souboru, zkontrolujte prosím, že nemáte otevřený soubor s"
                                  f"názvem Radomír Kocman-FV-{datetime.now(tz=UTC).strftime("%m-%Y")}.xml ve"
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
