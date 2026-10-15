"""Contains a class used to resolve paths to app resources, which differ in dev and prod."""
import sys
from pathlib import Path


class ResourceFinder:
    """Class used to resolve paths to the app resources on the computer, since these differ in dev and prod."""

    @staticmethod
    def resource_path(relative_path: Path) -> Path:
        """Get path to a resource, path resolution is needed, since paths are different in dev and prod environments.

        :param relative_path: Relative path to the resource, IE where it is.
        :return: Path to the resource during runtime.
        """
        try:
            base_path: Path = Path().resolve(sys._MEIPASS)
        except AttributeError:
            base_path: Path = Path().cwd()

        return base_path / relative_path
