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
from .utils import (
    GLOBAL_LOCK,
    is_provider,
    ensure_is_provider,
    is_delegated,
    represent_provider,
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

    'GLOBAL_LOCK',
    'is_provider',
    'ensure_is_provider',
    'is_delegated',
    'represent_provider',

    'Injection',
    'PositionalInjection',
    'NamedInjection',
)
