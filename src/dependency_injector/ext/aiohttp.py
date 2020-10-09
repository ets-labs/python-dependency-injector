"""Aiohttp extension module."""

from __future__ import absolute_import

import functools
import warnings

from dependency_injector import providers


warnings.warn(
    'Module "dependency_injector.ext.aiohttp" is deprecated since '
    'version 4.0.0. Use "dependency_injector.wiring" module instead.',
    category=DeprecationWarning,
)


class Application(providers.Singleton):
    """Aiohttp application provider."""


class Extension(providers.Singleton):
    """Aiohttp extension provider."""


class Middleware(providers.DelegatedCallable):
    """Aiohttp middleware provider."""

    __middleware_version__ = 1


class MiddlewareFactory(providers.Factory):
    """Aiohttp middleware factory provider."""


class View(providers.Callable):
    """Aiohttp view provider."""

    def as_view(self):
        """Return aiohttp view function."""
        @functools.wraps(self.provides)
        async def _view(request, *args, **kwargs):
            return await self.__call__(request, *args, **kwargs)
        return _view


class ClassBasedView(providers.Factory):
    """Aiohttp class-based view provider."""

    def as_view(self):
        """Return aiohttp view function."""
        async def _view(request, *args, **kwargs):
            return await self.__call__(request, *args, **kwargs)
        return _view
