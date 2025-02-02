"""Dependency injector errors."""


class Error(Exception):
    """Base error.

    All dependency injector errors extend this error class.
    """


class NoSuchProviderError(Error, AttributeError):
    """Error that is raised when provider lookup is failed."""


class NonCopyableArgumentError(Error):
    """Error that is raised when provider argument is not deep-copyable."""

    index: int
    keyword: str
    provider: object

    def __init__(self, provider: object, index: int = -1, keyword: str = "") -> None:
        self.provider = provider
        self.index = index
        self.keyword = keyword

    def __str__(self) -> str:
        s = (
            f"keyword argument {self.keyword}"
            if self.keyword
            else f"argument at index {self.index}"
        )
        return f"Couldn't copy {s} for provider {self.provider!r}"
