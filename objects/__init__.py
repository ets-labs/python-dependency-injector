"""
`Objects` library.
"""

from .catalog import Catalog
from .providers import (Provider, NewInstance, Singleton, Class, Object,
                        Function, Value)
from .injections import InitArg, Attribute, Method, inject


__all__ = ['Catalog',

           # Providers
           'Provider', 'NewInstance', 'Singleton', 'Class',
           'Object', 'Function', 'Value',

           # Injections
           'InitArg', 'Attribute', 'Method', 'inject']
