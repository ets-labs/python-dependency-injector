"""Dependency injector containers."""

from .declarative import (
    DeclarativeContainerMetaClass,
    DeclarativeContainer,
)
from .dynamic import (
    DynamicContainer,
)
from .utils import (
    is_container,
    override,
    copy,
)


# Set package name as a name of module for all public members of this package:
for item in (DeclarativeContainerMetaClass,
             DeclarativeContainer,
             DynamicContainer,
             is_container,
             override,
             copy,):
    item.__module__ = __name__


__all__ = (
    'DeclarativeContainerMetaClass',
    'DeclarativeContainer',

    'DynamicContainer',

    'is_container',
    'override',
    'copy',
)
