"""Contains a class with all the necessary methods and attributes for the app to run and handle user inputs."""
from __future__ import annotations

import multiprocessing as mp
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import Any

from customtkinter import CTk, CTkProgressBar  # type: ignore[import-untyped]

from enums.colour_enum import ColourEnum
from enums.err_no_enum import ErrNoEnum
from enums.queue_status import QueueStatus
from errors.app_error import AppError
from factories.script_factory import ScriptFactory
from scripts.kocman import Kocman  # noqa: F401 - ensures script subclasses are registered
from scripts.remove_ampersand import RemoveAmpersand  # noqa: F401
from services.script_process import ScriptProcess
from utils.error_handler import ErrorHandler
from utils.queue_message import QueueMessage
from utils.resource_finder import ResourceFinder
from utils.success_handler import SuccessHandler
from widgets.button_base import ButtonBase
from widgets.combo_box_base import ComboBoxBase
from widgets.frame_base import FrameBase
from widgets.label_base import LabelBase
from widgets.progressbar import ProgressBarBase


class XmlEditor(CTk):
    """Main app class responsible for rendering the app window and handling all user inputs."""

    def __init__(
            self,
    ) -> None:
        """Initialise the main app class.

        :return: None.
        """
        super().__init__()

        org_options: list[tuple[str, str]] = ScriptFactory.get_dropdown_options()
        self.__script_mapping: dict[str, str] = {
            display_name: key for key, display_name in org_options
        } | {key: key for key, _ in org_options}
        dropdown_values: list[str] = [display_name for _, display_name in org_options]

        self.__output_directory: Path = Path.cwd()
        self.__input_file: Path | None = None

        self.__inbound_queue: mp.Queue[QueueMessage | AppError] = mp.Queue()
        self.__outbound_queue: mp.Queue[QueueMessage] = mp.Queue()

        self.iconbitmap(
            bitmap=ResourceFinder.resource_path(Path("./resources/icon/xmlIcon.ico").resolve()),
        )

        self.title("XML Config")
        self.frame: FrameBase = FrameBase(
            master=self,
        )

        self.widgets: list[Any] = []

        self.load_xml: tuple[ButtonBase, LabelBase] = (
            ButtonBase(
                master=self.frame,
                command=self.open_xml,
                text="Načíst XML",
            ),
            LabelBase(
                master=self.frame,
                text="Nebyl načten žádný xml soubor",
                text_color=ColourEnum.RED,
            ),
        )
        self.widgets.append(
            self.load_xml,
        )
        self.drop_down: tuple[ComboBoxBase, LabelBase] = (
            ComboBoxBase(
                master=self.frame,
                values=dropdown_values,
            ),
            LabelBase(
                master=self.frame,
                text="",
            ),
        )
        max_label: str = max(dropdown_values, key=len) if dropdown_values else ""
        self.drop_down[0].configure(
            width=self.drop_down[0].cget(
                "font",
            ).measure(
                max_label,
            ) + 45)
        self.widgets.append(
            self.drop_down,
        )
        self.output_directory_widgets: tuple[ButtonBase, LabelBase] = (
            ButtonBase(
                master=self.frame,
                command=self.__choose_output_folder,
                text="Zvolit složku pro uložení výsledného souboru",
            ),
            LabelBase(
                master=self.frame,
                text=f"Složka pro uložení výsledného souboru: "
                     f"{self.__output_directory.name}",
                text_color=ColourEnum.GREEN,
            ),
        )
        self.widgets.append(self.output_directory_widgets)
        self.invoker: tuple[ButtonBase, LabelBase] = (
            ButtonBase(
                master=self.frame,
                command=self.threaded_invocation,
                text="Zpracovat XML",
            ),
            LabelBase(
                master=self.frame,
                text="",
            ),
        )
        self.widgets.append(self.invoker)

        self.frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.arrange_widgets(self.frame, self.widgets)

        self.progressbar: ProgressBarBase = ProgressBarBase(
            master=self.frame,
            mode="determinate",
        )

    @staticmethod
    def arrange_widgets(master: FrameBase, widgets: list[tuple[Any, Any]]) -> None:
        """Arrange widgets into a 2xX grid within the master widgets.

        :param master: The master widget within which to arrange all the child widgets.
        :param widgets: List of all child widgets, expected to be arranged into a list of tuples, where each list item
                        represents a row and each tuple item represents a column within the grid.
        :return: None.
        """
        for i, row in enumerate(widgets):
            for j, widget in enumerate(row):
                widget.grid(
                    row=i,
                    column=j,
                    padx=10,
                    pady=10,
                )
                master.columnconfigure(j, weight=1)
            master.rowconfigure(i, weight=1)

    def open_xml(self) -> None:
        """Open a dialogue letting the user choose the input and open said input.

        :return: None.
        """
        file_types = [("XML soubor", "*.xml")]
        filename: str = filedialog.askopenfilename(
            filetypes=file_types,
            initialdir=Path.cwd(),
        )

        if not filename:
            return

        self.__input_file = Path(filename)

        self.load_xml[1].configure(
            text=f"Soubor {self.__input_file.name} úspěšně načten",
            text_color="green",
        )

    def __choose_output_folder(self) -> None:
        """Let the user select an output folder.

        Displays a pop-up window to the user, allowing them to select a folder to save the output into.
        :return: None.
        """
        try:
            folder: str = filedialog.askdirectory(
                initialdir=Path.cwd(),
            )

            if not folder:
                return

            output_directory: Path = Path(folder).resolve()

            if not output_directory.exists():
                return

            self.__output_directory = output_directory
            self.output_directory_widgets[1].configure(
                text=f"Složka pro uložení výsledného souboru: {self.__output_directory.name}",
                text_color="green",
            )

        except FileNotFoundError:
            ErrorHandler(
                error_message="Chyba při načítání výstupní složky",
                error_code=2,
            ).lift()
            self.output_directory_widgets[1].configure(
                text="Chyba při načítání výstupní složky",
                text_color="red",
            )
            return

    def threaded_invocation(self) -> None:
        """Invoke the underlying script in a background process to ensure GUI does not lock up.

        :return: None.
        """
        if self.__input_file is None:
            ErrorHandler(
                error_message="Nebyl načten žádný XML soubor!",
                error_code=1,
            ).lift()
            return

        selected_label: str = self.drop_down[0].get()
        script_key: str = self.__script_mapping.get(selected_label, selected_label)
        if not script_key:
            ErrorHandler(
                error_message="Nebyla vybrána žádná organizace!",
                error_code=2,
            ).lift()
            return

        self.invoker[1].configure(text="")
        self.update_idletasks()
        self.progressbar.grid(
            row=self.invoker[1].grid_info()["row"],
            column=self.invoker[1].grid_info()["column"],
        )

        self.__block_start_button()

        queue_thread: threading.Thread = threading.Thread(
            target=self.__queue_listener,
            daemon=True,
        )
        queue_thread.start()

        try:
            worker_process = ScriptProcess(
                script_key=script_key,
                input_file=self.__input_file,
                output_folder=self.__output_directory,
                inbound_queue=self.__outbound_queue,
                outbound_queue=self.__inbound_queue,
            )
            worker_process.start()

        except AppError as e:
            ErrorHandler(
                error_message=e.error_message,
                error_code=e.error_code,
            )

    def __unblock_start_button(self) -> None:
        """Unblock the start button used to invoke the script.

        Enables the button used to start the script.
        :return: None.
        """
        self.invoker[0].configure(
            state=tk.NORMAL,
        )

    def __block_start_button(self) -> None:
        """Block the start button used to invoke the script.

        Disables the button used to start the script.
        :return: None.
        """
        self.invoker[0].configure(
            state=tk.DISABLED,
        )

    def __queue_listener(self) -> None:
        """Run a background thread listening for events in the queue.

        :return: None.
        """
        while True:
            msg: QueueMessage | AppError = self.__inbound_queue.get()

            if isinstance(msg, QueueMessage):
                match msg.status:
                    case QueueStatus.PROGRESS:
                        self.after(0, self.progressbar.set, msg.payload)

                    case QueueStatus.FINISHED:
                        self.__unblock_start_button()
                        self.after(0, self.progressbar.grid_forget)
                        self.after(0, self.progressbar.set, 0.0)
                        self.invoker[1].configure(
                            text="Hurá!",
                            text_color=ColourEnum.GREEN,
                        )

                        if msg.payload is None:
                            raise AppError(
                                error_code=ErrNoEnum.PAYLOAD_IN_QUEUE_IS_NONE,
                                error_message="Vnitřní chyba programu, zkuste to prosím znovu.",
                            )

                        SuccessHandler(msg.payload)
                        return

                if isinstance(msg, AppError):
                    self.__unblock_start_button()
                    self.after(0, self.progressbar.grid_forget)
                    self.after(0, self.progressbar.set, 0.0)
                    self.invoker[1].configure(
                        text=msg.error_message,
                    )
                    ErrorHandler(
                        error_code=msg.error_code,
                        error_message=msg.error_message,
                    )
                    return

            if isinstance(msg, AppError):
                self.__unblock_start_button()
                self.progressbar.grid_forget()
                self.invoker[1].configure(
                    text=msg.error_message,
                )
                ErrorHandler(
                    error_code=msg.error_code,
                    error_message=msg.error_message,
                )
                return

            self.progressbar.after(
                0,
                self.progressbar.set,
                msg.payload,
            )

    def __send_msg(
            self,
            msg: QueueMessage,
    ) -> None:
        """Send a message to the background process through the queue.

        :param msg: Message to be sent.
        :return: None.
        """
        self.__outbound_queue.put(msg)
