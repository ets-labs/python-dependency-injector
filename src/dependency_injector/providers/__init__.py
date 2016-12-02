"""Dependency injector providers."""

from .base import (
    Provider,
    Object,
    Delegate,
    ExternalDependency,
    OverridingContext,
)
from .configuration import (
    Configuration,
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
from .injections import (
    Injection,
    PositionalInjection,
    NamedInjection,
)
from .utils import (
    is_provider,
    ensure_is_provider,
    is_delegated,
    represent_provider,
    deepcopy,
)


__all__ = (
    'Provider',
    'Object',
    'Delegate',
    'ExternalDependency',
    'OverridingContext',

    'Configuration',

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

    'Injection',
    'PositionalInjection',
    'NamedInjection',

    'is_provider',
    'ensure_is_provider',
    'is_delegated',
    'represent_provider',
    'deepcopy',
)
