from typing import Any, Callable as _Callable, Optional, TypeVar, Union

from flask.wrappers import Request

from dependency_injector import providers

request: providers.Object[Request]
T = TypeVar("T")

class Application(providers.Singleton[T]): ...
class Extension(providers.Singleton[T]): ...

class View(providers.Callable[T]):
    def as_view(self) -> _Callable[..., T]: ...

class ClassBasedView(providers.Factory[T]):
    def as_view(self, name: str) -> _Callable[..., T]: ...

def as_view(
    provider: Union[View[T], ClassBasedView[T]], name: Optional[str] = None
) -> _Callable[..., T]: ...
