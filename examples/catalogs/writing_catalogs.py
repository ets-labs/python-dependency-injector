"""Catalog example."""

import dependency_injector as di


class Catalog(di.AbstractCatalog):
    """Providers catalog."""

    factory1 = di.Factory(object)
    """:type: (di.Provider) -> object"""

    factory2 = di.Factory(object)
    """:type: (di.Provider) -> object"""

# Creating some objects:
object1 = Catalog.factory1()
object2 = Catalog.factory2()

# Making some asserts:
assert object1 is not object2
assert isinstance(object1, object)
assert isinstance(object2, object)
