"""Dependency injector."""

from dependency_injector.catalogs import (
    DeclarativeCatalog,
    AbstractCatalog,
    DynamicCatalog,
    CatalogBundle,
    override,
)

from dependency_injector.providers import (
    Provider,
    Delegate,
    Callable,
    DelegatedCallable,
    Factory,
    DelegatedFactory,
    Singleton,
    DelegatedSingleton,
    ExternalDependency,
    StaticProvider,
    Class,
    Object,
    Function,
    Value,
    Config,
)

from dependency_injector.injections import (
    Injection,
    Arg,
    KwArg,
    Attribute,
    Method,
    inject,
)

from dependency_injector.utils import (
    is_provider,
    ensure_is_provider,
    is_delegated_provider,
    is_injection,
    ensure_is_injection,
    is_arg_injection,
    is_kwarg_injection,
    is_attribute_injection,
    is_method_injection,
    is_catalog,
    is_dynamic_catalog,
    is_declarative_catalog,
    is_catalog_bundle,
    ensure_is_catalog_bundle,
)

from dependency_injector.errors import (
    Error,
    UndefinedProviderError,
)

# Backward compatibility for versions < 0.11.*
from dependency_injector import catalogs
catalog = catalogs

VERSION = '1.16.2'
"""Version number that follows semantic versioning.

:type: str
"""


__all__ = (
    # Catalogs
    'DeclarativeCatalog',
    'AbstractCatalog',
    'DynamicCatalog',
    'CatalogBundle',
    'override',

    # Providers
    'Provider',
    'Delegate',
    'Callable',
    'DelegatedCallable',
    'Factory',
    'DelegatedFactory',
    'Singleton',
    'DelegatedSingleton',
    'ExternalDependency',
    'StaticProvider',
    'Class',
    'Object',
    'Function',
    'Value',
    'Config',

    # Injections
    'Injection',
    'Arg',
    'KwArg',
    'Attribute',
    'Method',
    'inject',

    # Utils
    'is_provider',
    'ensure_is_provider',
    'is_delegated_provider',
    'is_injection',
    'ensure_is_injection',
    'is_arg_injection',
    'is_kwarg_injection',
    'is_attribute_injection',
    'is_method_injection',
    'is_catalog',
    'is_dynamic_catalog',
    'is_declarative_catalog',
    'is_catalog_bundle',
    'ensure_is_catalog_bundle',

    # Errors
    'Error',
    'UndefinedProviderError',

    # Version
    'VERSION'
)
