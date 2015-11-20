"""Declarative catalog overriding using `@override()` decorator example."""

import collections

from dependency_injector import catalogs
from dependency_injector import providers

# Creating some example classes:
Object1 = collections.namedtuple('Object1', ['arg1', 'arg2'])
Object2 = collections.namedtuple('Object2', ['object1'])
ExtendedObject2 = collections.namedtuple('ExtendedObject2', [])


class Catalog(catalogs.DeclarativeCatalog):
    """Catalog of some providers."""

    object1_factory = providers.Factory(Object1,
                                        arg1=1,
                                        arg2=2)
    """:type: providers.Provider -> Object1"""

    object2_factory = providers.Factory(Object2,
                                        object1=object1_factory)
    """:type: providers.Provider -> Object2"""


# Overriding `Catalog` with `AnotherCatalog`:
@catalogs.override(Catalog)
class AnotherCatalog(catalogs.DeclarativeCatalog):
    """Overriding catalog."""

    object2_factory = providers.Factory(ExtendedObject2)
    """:type: providers.Provider -> ExtendedObject2"""


# Creating some objects using overridden catalog:
object2_1 = Catalog.object2_factory()
object2_2 = Catalog.object2_factory()

# Making some asserts:
assert Catalog.is_overridden

assert object2_1 is not object2_2

assert isinstance(object2_1, ExtendedObject2)
assert isinstance(object2_2, ExtendedObject2)
