"""
`Objects` library.
"""

from .catalog import Catalog
from .std_providers import (Provider, NewInstance, Singleton, Class, Object,
                            Function, Value)


__all__ = ['Catalog', 'Provider', 'NewInstance', 'Singleton', 'Class',
           'Object', 'Function', 'Value']
