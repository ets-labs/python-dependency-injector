"""Resources module."""

import abc
from typing import TypeVar, Generic


T = TypeVar('T')


class Resource(Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def init(self, *args, **kwargs) -> T:
        ...

    @abc.abstractmethod
    def shutdown(self, resource: T) -> None:
        ...


class AsyncResource(Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def init(self, *args, **kwargs) -> T:
        ...

    @abc.abstractmethod
    async def shutdown(self, resource: T) -> None:
        ...
