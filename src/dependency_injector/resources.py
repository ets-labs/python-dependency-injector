"""Resources module."""

import abc
import sys
from typing import TypeVar, Generic

if sys.version_info < (3, 7):
    from typing import GenericMeta
else:
    class GenericMeta(type):
        ...


T = TypeVar('T')


class ResourceMeta(GenericMeta, abc.ABCMeta):
    def __getitem__(cls, item):
        # Spike for Python 3.6
        return cls(item)


class Resource(Generic[T], metaclass=ResourceMeta):

    @abc.abstractmethod
    def init(self, *args, **kwargs) -> T:
        ...

    @abc.abstractmethod
    def shutdown(self, resource: T) -> None:
        ...


class AsyncResource(Generic[T], metaclass=ResourceMeta):

    @abc.abstractmethod
    async def init(self, *args, **kwargs) -> T:
        ...

    @abc.abstractmethod
    async def shutdown(self, resource: T) -> None:
        ...
