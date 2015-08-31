"""Operating with catalog providers example."""

from dependency_injector.catalog import AbstractCatalog
from dependency_injector.providers import Factory
from dependency_injector.providers import Singleton


class Catalog(AbstractCatalog):

    """Providers catalog."""

    provider1 = Factory(object)
    """:type: (dependency_injector.Provider) -> object"""

    provider2 = Factory(object)
    """:type: (dependency_injector.Provider) -> object"""

    provider3 = Singleton(object)
    """:type: (dependency_injector.Provider) -> object"""

    provider4 = Singleton(object)
    """:type: (dependency_injector.Provider) -> object"""


# Making some asserts:
assert Catalog.providers == dict(provider1=Catalog.provider1,
                                 provider2=Catalog.provider2,
                                 provider3=Catalog.provider3,
                                 provider4=Catalog.provider4)
assert Catalog.filter(Factory) == dict(provider1=Catalog.provider1,
                                       provider2=Catalog.provider2)
assert Catalog.filter(Singleton) == dict(provider3=Catalog.provider3,
                                         provider4=Catalog.provider4)
