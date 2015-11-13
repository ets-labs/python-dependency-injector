"""Errors module."""


class Error(Exception):
    """Base error."""


class UndefinedProviderError(Error, AttributeError):
    """Undefined provider error."""
