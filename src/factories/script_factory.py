"""Contains a factory used to create and register new scripts in the ScriptBase repository for easy expandability."""
from scripts.script_base import ScriptBase


class ScriptFactory:
    """Factory used to create and register new scripts in the ScriptBase repository for easy expandability."""

    @classmethod
    def get_dropdown_options(cls) -> list[tuple[str, str]]:
        """Return [(key, label)] pairs for scripts to populate the UI dropdown menu.

        :return: List of (key, label) pairs for populating the UI dropdown menu.
        """
        return [(key, script.display_name) for key, script in ScriptBase.registry.items()]

    @classmethod
    def create(
            cls,
            key: str,
            *args,
            **kwargs,
        ) -> ScriptBase:
        """Instantiate a new script object based on the key passed to the repository.

        :param key: Key to search for in the repository.
        :param args: Positional arguments to initialise the script object with.
        :param kwargs: Keyword arguments to initialise the script object with.
        :return: New script object.
        """
        target_class = ScriptBase.registry.get(key)
        if not target_class:
            msg: str = f"Unknown script: {key}. Available: {list(ScriptBase.registry)}"
            raise ValueError(msg)
        return target_class(*args, **kwargs)
