"""Contains a class used to write ElementTrees into XML files."""
import xml.etree.ElementTree as ET
from pathlib import Path


class XMLWriter:
    """FileWriter class used to write ElementTrees into XML output files."""

    def write(
            self,
            path: Path,
            data: ET.ElementTree,
    ) -> None:
        """Write the provided element tree into the output file located at path.

        :param path: Path to the output file.
        :param data: Element tree to be written into the output file.
        :return: None.
        """
        data.write(
            file_or_filename=str(path),
            encoding="UTF-8",
            xml_declaration=True,
        )
