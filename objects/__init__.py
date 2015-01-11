"""
`Objects` library.
"""

from .catalog import Catalog, overrides
from .providers import (Provider, NewInstance, Singleton, Class, Object,
                        Function, Value)
from .injections import InitArg, Attribute, Method, uses


__all__ = ['Catalog', 'overrides',

           # Providers
           'Provider', 'NewInstance', 'Singleton', 'Class',
           'Object', 'Function', 'Value',

           # Injections
           'InitArg', 'Attribute', 'Method', 'uses']
