"""Dependency injector providers package."""

from dependency_injector.providers.base import (
    Provider,
    Delegate,
    Static,
    StaticProvider,
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
)
from dependency_injector.providers.static import (
    Object,
    Value,
    Class,
    Function,
)
from dependency_injector.providers.config import (
    Config,
    ChildConfig,
)


__all__ = (
    'Provider',
    'Delegate',
    'Static', 'StaticProvider',
    'ExternalDependency',

    'Callable',
    'DelegatedCallable',

    'Factory',
    'DelegatedFactory',
    'Singleton',
    'DelegatedSingleton',

    'Object',
    'Value',
    'Class',
    'Function',

    'Config',
    'ChildConfig',

    'OverridingContext',
    'override',
)
