"""Flask extension module."""

from __future__ import absolute_import
import warnings

from flask import request as flask_request

from dependency_injector import providers, errors


warnings.warn(
    'Module "dependency_injector.ext.aiohttp" is deprecated since '
    'version 4.0.0. Use "dependency_injector.wiring" module instead.',
    category=DeprecationWarning,
)


request = providers.Object(flask_request)


class Application(providers.Singleton):
    """Flask application provider."""


class Extension(providers.Singleton):
    """Flask extension provider."""


class View(providers.Callable):
    """Flask view provider."""

    def as_view(self):
        """Return Flask view function."""
        return as_view(self)


class ClassBasedView(providers.Factory):
    """Flask class-based view provider."""

    def as_view(self, name):
        """Return Flask view function."""
        return as_view(self, name)


def as_view(provider, name=None):
    """Transform class-based view provider to view function."""
    if isinstance(provider, providers.Factory):
        def view(*args, **kwargs):
            self = provider()
            return self.dispatch_request(*args, **kwargs)

        assert name, 'Argument "endpoint" is required for class-based views'
        view.__name__ = name
    elif isinstance(provider, providers.Callable):
        def view(*args, **kwargs):
            return provider(*args, **kwargs)

        view.__name__ = provider.provides.__name__
    else:
        raise errors.Error('Undefined provider type')

    view.__doc__ = provider.provides.__doc__
    view.__module__ = provider.provides.__module__

    if isinstance(provider.provides, type):
        view.view_class = provider.provides

    if hasattr(provider.provides, 'decorators'):
        for decorator in provider.provides.decorators:
            view = decorator(view)

    if hasattr(provider.provides, 'methods'):
        view.methods = provider.provides.methods

    if hasattr(provider.provides, 'provide_automatic_options'):
        view.provide_automatic_options = provider.provides.provide_automatic_options

    return view
