"""Objects.

Dependency management tool for Python projects.
"""

from .catalog import AbstractCatalog
from .catalog import override

from .providers import Provider
from .providers import Delegate
from .providers import NewInstance
from .providers import Singleton
from .providers import ExternalDependency
from .providers import Class
from .providers import Object
from .providers import Function
from .providers import Value
from .providers import Callable
from .providers import Config

from .injections import KwArg
from .injections import Attribute
from .injections import Method

from .errors import Error


__all__ = ('AbstractCatalog',
           'override',

           # Providers
           'Provider',
           'Delegate',
           'NewInstance',
           'Singleton',
           'ExternalDependency',
           'Class',
           'Object',
           'Function',
           'Value',
           'Callable',
           'Config',

           # Injections
           'KwArg',
           'Attribute',
           'Method',

           # Errors
           'Error')
