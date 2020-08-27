from typing import Awaitable as _Awaitable

from dependency_injector import providers


class Application(providers.Singleton): ...


class Extension(providers.Singleton): ...


class Middleware(providers.DelegatedCallable): ...


class MiddlewareFactory(providers.Factory): ...


class View(providers.Callable):
    def as_view(self) -> _Awaitable: ...


class ClassBasedView(providers.Factory):
    def as_view(self) -> _Awaitable: ...
