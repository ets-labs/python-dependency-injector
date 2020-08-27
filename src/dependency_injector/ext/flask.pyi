from typing import Union, Optional, Callable as _Callable, Any

from flask import request as flask_request
from dependency_injector import providers


request: providers.Object[flask_request]


class Application(providers.Singleton): ...


class Extension(providers.Singleton): ...


class View(providers.Callable):
    def as_view(self) -> _Callable[..., Any]: ...


class ClassBasedView(providers.Factory):
    def as_view(self, name: str) -> _Callable[..., Any]: ...


def as_view(provider: Union[View, ClassBasedView], name: Optional[str] = None) -> _Callable[..., Any]: ...
