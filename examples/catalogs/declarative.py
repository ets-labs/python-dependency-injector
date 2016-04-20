"""Declarative catalog simple example."""

from dependency_injector import catalogs
from dependency_injector import providers


# Defining declarative catalog:
class Catalog(catalogs.DeclarativeCatalog):
    """Providers catalog."""

    factory1 = providers.Factory(object)

    factory2 = providers.Factory(object)

# Creating some objects:
object1 = Catalog.factory1()
object2 = Catalog.factory2()

# Making some asserts:
assert object1 is not object2
assert isinstance(object1, object)
assert isinstance(object2, object)
