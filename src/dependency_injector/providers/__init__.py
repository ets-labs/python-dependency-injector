"""Dependency injector providers."""

from .base import (
    Provider,
)
from .callables import (
    Callable,
    DelegatedCallable,
)
from .factories import (
    Factory,
    DelegatedFactory,
)
from .singletons import (
    BaseSingleton,

    Singleton,
    DelegatedSingleton,

    ThreadSafeSingleton,
    DelegatedThreadSafeSingleton,

    ThreadLocalSingleton,
    DelegatedThreadLocalSingleton,
)
from .static import (
    Object,
    Delegate,
    ExternalDependency,
)
from .injections import (
    Injection,
    PositionalInjection,
    NamedInjection,
)
from .utils import (
    GLOBAL_LOCK,
    OverridingContext,
    is_provider,
    ensure_is_provider,
    is_delegated,
    represent_provider,
)


__all__ = (
    'Provider',

    'Callable',
    'DelegatedCallable',

    'Factory',
    'DelegatedFactory',

    'BaseSingleton',

    'Singleton',
    'DelegatedSingleton',

    'ThreadSafeSingleton',
    'DelegatedThreadSafeSingleton',

    'ThreadLocalSingleton',
    'DelegatedThreadLocalSingleton',

    'Object',
    'Delegate',
    'ExternalDependency',

    'Injection',
    'PositionalInjection',
    'NamedInjection',

    'GLOBAL_LOCK',
    'OverridingContext',
    'is_provider',
    'ensure_is_provider',
    'is_delegated',
    'represent_provider',
)
