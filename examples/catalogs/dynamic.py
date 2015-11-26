"""Dynamic catalog simple example."""

from dependency_injector import catalogs
from dependency_injector import providers


# Defining dynamic catalog:
catalog = catalogs.DynamicCatalog(factory1=providers.Factory(object),
                                  factory2=providers.Factory(object))

# Creating some objects:
object1 = catalog.factory1()
object2 = catalog.factory2()

# Making some asserts:
assert object1 is not object2
assert isinstance(object1, object)
assert isinstance(object2, object)
