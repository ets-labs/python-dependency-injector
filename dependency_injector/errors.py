"""Errors module."""


class Error(Exception):
    """Base error.

    All dependency injector errors extend this error class.
    """


class UndefinedProviderError(Error, AttributeError):
    """Undefined provider error.

    This error is used when provider could not be defined, for example:

        - provider with certain name could not be defined
        - catalog's name of the certain provider could not be defined
        - etc...

    Also this error extends standard :py:class:`AttributeError`. This gives
    possibility to use it correctly with ``__getattr__()``.
    """
