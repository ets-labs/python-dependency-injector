"""Objects."""

from .catalog import AbstractCatalog, overrides
from .providers import (Provider, NewInstance, Singleton, Class, Object,
                        Function, Value)
from .injections import InitArg, Attribute, Method


__all__ = ('AbstractCatalog', 'overrides',

           # Providers
           'Provider', 'NewInstance', 'Singleton', 'Class',
           'Object', 'Function', 'Value',

           # Injections
           'InitArg', 'Attribute', 'Method')
