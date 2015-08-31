"""`Catalog.override()` example."""

from collections import namedtuple

from dependency_injector.catalog import AbstractCatalog
from dependency_injector.providers import Factory
from dependency_injector.injections import KwArg


# Creating some example classes:
Object1 = namedtuple('Object1', ['arg1', 'arg2'])
Object2 = namedtuple('Object2', ['object1'])
ExtendedObject2 = namedtuple('ExtendedObject2', [])


class Catalog(AbstractCatalog):

    """Providers catalog."""

    object1_factory = Factory(Object1,
                              KwArg('arg1', 1),
                              KwArg('arg2', 2))
    """:type: (dependency_injector.Provider) -> Object1"""

    object2_factory = Factory(Object2,
                              KwArg('object1', object1_factory))
    """:type: (dependency_injector.Provider) -> Object2"""


class AnotherCatalog(AbstractCatalog):

    """Another providers catalog."""

    object2_factory = Factory(ExtendedObject2)
    """:type: (dependency_injector.Provider) -> ExtendedObject2"""


# Overriding `Catalog` with `AnotherCatalog`:
Catalog.override(AnotherCatalog)

# Creating some dependency_injector using overridden catalog:
object2_1 = Catalog.object2_factory()
object2_2 = Catalog.object2_factory()

# Making some asserts:
assert object2_1 is not object2_2

assert isinstance(object2_1, ExtendedObject2)
assert isinstance(object2_2, ExtendedObject2)
