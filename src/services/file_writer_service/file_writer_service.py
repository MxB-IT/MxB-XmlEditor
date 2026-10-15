"""Contains the registry used as a flexible and expandable FileWriterService."""
from enums.file_type import FileType
from services.file_writer_service.file_writer_strategy import FileWriterStrategy
from pathlib import Path
from typing import Any


class FileWriterService:
    def __init__(
            self,
    ) -> None:
        """Initialise the FileWriterService class.

        Initialises the class and the internal private writers instance attribute.
        :return: None.
        """
        self._writers: dict[FileType, FileWriterStrategy] = {}

    def register_writer(
            self,
            file_type: FileType,
            writer: FileWriterStrategy,
    ) -> None:
        """Add a new FileWriter into the FileWriter registry inside this class.

        :param file_type: Filetype the newly registered FileWriter is able to service.
        :param writer: Reference to the FileWriter class.
        :return: None.
        """
        self._writers[file_type] = writer

    def write_file(
            self,
            path: str | Path,
            data: Any,
            file_type: FileType,
    ) -> None:
        """Write the data provided into a file at the specified filepath, creating the file if necessary.

        :param path: Path to the output file.
        :param data: Data to write into the output file.
        :param file_type: FileType value representing the type of file to write the data into.
        :return:
        """
        if file_type not in self._writers:
            raise ValueError

        self._writers[file_type].write(
            path=Path(path),
            data=data,
        )
