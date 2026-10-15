"""Contains a class used to write strings into output files."""
from pathlib import Path


class StringWriter:
    """Writer class used to write strings into output files."""

    def write(
            self,
            path: Path,
            data: str,
    ) -> None:
        """Write the provided string into the output file located at path.

        :param path: Path to the output file.
        :param data: String to be written into the output file.
        :return: None.
        """
        path.write_text(
            data=data,
            encoding="UTF-8",
        )
