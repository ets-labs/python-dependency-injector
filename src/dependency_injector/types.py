from typing import TypeVar, Generic, Any


Injection = Any
T = TypeVar('T')


class Provider(Generic[T]):
    def __call__(self, *args: Injection, **kwargs: Injection) -> T: ...
