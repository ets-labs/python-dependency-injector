"""Dependency injector providers package."""

from dependency_injector.providers.base import (
    Provider,
    Delegate,
    Object,
    ExternalDependency,
    OverridingContext,
    override,
)
from dependency_injector.providers.callable import (
    Callable,
    DelegatedCallable,
)
from dependency_injector.providers.creational import (
    Factory,
    DelegatedFactory,
    Singleton,
    DelegatedSingleton,
    ThreadLocalSingleton,
    DelegatedThreadLocalSingleton
)


__all__ = (
    'Provider',
    'Delegate',
    'Object',
    'ExternalDependency',

    'OverridingContext',
    'override',

    'Callable',
    'DelegatedCallable',

    'Factory',
    'DelegatedFactory',

    'Singleton',
    'DelegatedSingleton',

    'ThreadLocalSingleton',
    'DelegatedThreadLocalSingleton',
)
