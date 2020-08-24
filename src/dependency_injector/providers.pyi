from typing import TypeVar, Generic, Callable, Any

Injection = Any
T = TypeVar('T')


class Factory(Generic[T]):

    def __init__(self, provides: Callable[..., T], *args: Injection, **kwargs: Injection) -> None: ...
    def __call__(self, *args: Injection, **kwargs: Injection) -> T: ...
