"""Dependency injector errors."""


class Error(Exception):
    """Base error.

    All dependency injector errors extend this error class.
    """


class NoSuchProviderError(Error, AttributeError):
    """Error that is raised when provider lookup is failed."""
