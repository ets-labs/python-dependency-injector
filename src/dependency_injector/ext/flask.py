"""Flask extension module."""

from __future__ import absolute_import

from flask import Flask

from dependency_injector import providers, errors


def create_app(name, routes, **kwargs):
    """Create Flask app and add routes."""
    app = Flask(name, **kwargs)
    for route in routes:
        app.add_url_rule(*route.args, **route.options)
    return app


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


class Route:
    """Route is a glue for Dependency Injector providers and Flask views."""

    def __init__(
            self,
            rule,
            endpoint=None,
            view_provider=None,
            provide_automatic_options=None,
            **options):
        """Initialize route."""
        self.view_provider = view_provider
        self.args = (rule, endpoint, as_view(view_provider, endpoint), provide_automatic_options)
        self.options = options

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        rule, endpoint, _, provide_automatic_options = self.args
        view_provider = providers.deepcopy(self.view_provider, memo)

        return self.__class__(
            rule,
            endpoint,
            view_provider,
            provide_automatic_options,
            **self.options)
