"""Dependency injector providers."""

from .base import (
    Provider,
    Delegate,
    Object,
    ExternalDependency,
    OverridingContext,
    override,
)
from .callable import (
    Callable,
    DelegatedCallable,
)
from .creational import (
    Factory,
    DelegatedFactory,
    Singleton,
    DelegatedSingleton,
    ThreadLocalSingleton,
    DelegatedThreadLocalSingleton,
)
from .injections import (
    Injection,
    PositionalInjection,
    NamedInjection,
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

    'Injection',
    'PositionalInjection',
    'NamedInjection',
)
