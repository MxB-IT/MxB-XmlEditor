"""Contains a class defining the interface for all writers."""
from pathlib import Path
from typing import Any, Protocol


class FileWriterStrategy(Protocol):
    """Interface for all the FileWriter classes."""

    def write(
            self,
            path: Path,
            data: Any,
    ) -> None:
        """Write data to the specified filepath.

        Takes the provided data and writes them into the specified filepath.
        :param path: Path to the file into which the data shall be written.
        :param data: Data to write into the output file.
        :return: None.
        """
