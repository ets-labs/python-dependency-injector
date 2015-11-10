"""Dependency injector."""

from .catalogs import DeclarativeCatalog
from .catalogs import AbstractCatalog
from .catalogs import DynamicCatalog
from .catalogs import CatalogBundle
from .catalogs import override

from .providers import Provider
from .providers import Delegate
from .providers import Factory
from .providers import Singleton
from .providers import ExternalDependency
from .providers import StaticProvider
from .providers import Class
from .providers import Object
from .providers import Function
from .providers import Value
from .providers import Callable
from .providers import Config

from .injections import Injection
from .injections import Arg
from .injections import KwArg
from .injections import Attribute
from .injections import Method
from .injections import inject

from .utils import is_provider
from .utils import ensure_is_provider
from .utils import is_injection
from .utils import ensure_is_injection
from .utils import is_arg_injection
from .utils import is_kwarg_injection
from .utils import is_attribute_injection
from .utils import is_method_injection
from .utils import is_catalog
from .utils import is_dynamic_catalog
from .utils import is_declarative_catalog
from .utils import is_catalog_bundle
from .utils import ensure_is_catalog_bundle

from .errors import Error

# Backward compatibility for versions < 0.11.*
from . import catalogs
catalog = catalogs

VERSION = '0.10.5'


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
    'Factory',
    'Singleton',
    'ExternalDependency',
    'StaticProvider',
    'Class',
    'Object',
    'Function',
    'Value',
    'Callable',
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

    # Version
    'VERSION'
)
