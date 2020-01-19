"""Exceptions used in API routes."""


class ApiException(Exception):
    """The base class for API exceptions."""

    def __init__(self, message="Invalid request.", code=400):
        """Create a new ApiException."""
        self.message = message
        self.code = code

    def __str__(self):
        """Show the ApiException message when printed."""
        return self.message


class FileTooLargeException(ApiException):
    """Raised when an uploaded file is too large."""

    def __init__(self):
        """Create a new FileTooLargeException."""
        self.message = "The uploaded file exceeds the maximum file size."
        self.code = 400
