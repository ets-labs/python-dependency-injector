"""Objects.

Dependency management tool for Python projects.
"""

from .catalog import AbstractCatalog

from .providers import Provider
from .providers import Delegate
from .providers import Factory
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

from .decorators import override
from .decorators import inject

from .errors import Error


__all__ = ('AbstractCatalog',

           # Providers
           'Provider',
           'Delegate',
           'Factory',
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

           # Decorators
           'override',
           'inject',

           # Errors
           'Error')
