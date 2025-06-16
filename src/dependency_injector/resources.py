"""Resources module."""

from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, Generic, Optional, Tuple, TypeVar

T = TypeVar("T")


class Resource(Generic[T], metaclass=ABCMeta):
    __slots__: ClassVar[Tuple[str, ...]] = ("args", "kwargs", "obj")

    obj: Optional[T]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.obj = None

    @abstractmethod
    def init(self, *args: Any, **kwargs: Any) -> Optional[T]: ...

    def shutdown(self, resource: Optional[T]) -> None: ...

    def __enter__(self) -> Optional[T]:
        self.obj = obj = self.init(*self.args, **self.kwargs)
        return obj

    def __exit__(self, *exc_info: Any) -> None:
        self.shutdown(self.obj)
        self.obj = None


class AsyncResource(Generic[T], metaclass=ABCMeta):
    __slots__: ClassVar[Tuple[str, ...]] = ("args", "kwargs", "obj")

    obj: Optional[T]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.obj = None

    @abstractmethod
    async def init(self, *args: Any, **kwargs: Any) -> Optional[T]: ...

    async def shutdown(self, resource: Optional[T]) -> None: ...

    async def __aenter__(self) -> Optional[T]:
        self.obj = obj = await self.init(*self.args, **self.kwargs)
        return obj

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.shutdown(self.obj)
        self.obj = None
