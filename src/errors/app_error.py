"""Contains a class used to raise any and all app errors that should propagate up."""
from enums.err_no_enum import ErrNoEnum


class AppError(Exception):
    """Represents all errors raised by the app voluntarily."""

    def __init__(
            self,
            error_message: str,
            error_code: ErrNoEnum,
    ) -> None:
        """Initialise the AppError class.

        Inititalises the AppError class, setting its internal attributes, utilising the error message and error code
        passed.
        :param error_message: Error message to be shown to the user upon propagating the error to the GUI layer.
        :param error_code: Error code for the error raised to help identify what raised this error.
        """
        super().__init__(error_message, error_code)
        self.error_message: str = error_message
        """Error message to be shown to the user in relation to the raised error."""

        self.error_code: ErrNoEnum = error_code
        """Error code exactly identifying the error raised."""
