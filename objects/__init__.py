"""Objects."""

from .catalog import AbstractCatalog, overrides

from .providers import Provider
from .providers import Delegate
from .providers import NewInstance
from .providers import Singleton
from .providers import Scoped
from .providers import ExternalDependency
from .providers import Class
from .providers import Object
from .providers import Function
from .providers import Value
from .providers import Callable
from .providers import Config

from .injections import InitArg
from .injections import Attribute
from .injections import Method

from .errors import Error


__all__ = ('AbstractCatalog',
           'overrides',

           # Providers
           'Provider',
           'Delegate',
           'NewInstance',
           'Singleton',
           'Scoped',
           'ExternalDependency',
           'Class',
           'Object',
           'Function',
           'Value',
           'Callable',
           'Config',

           # Injections
           'InitArg',
           'Attribute',
           'Method',

           # Errors
           'Error')
