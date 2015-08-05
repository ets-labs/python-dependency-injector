"""Operating with catalog providers example."""

from objects.catalog import AbstractCatalog
from objects.providers import Factory
from objects.providers import Singleton


class Catalog(AbstractCatalog):

    """Providers catalog."""

    provider1 = Factory(object)
    """:type: (objects.Provider) -> object"""

    provider2 = Factory(object)
    """:type: (objects.Provider) -> object"""

    provider3 = Singleton(object)
    """:type: (objects.Provider) -> object"""

    provider4 = Singleton(object)
    """:type: (objects.Provider) -> object"""


# Making some asserts:
assert Catalog.providers == dict(provider1=Catalog.provider1,
                                 provider2=Catalog.provider2,
                                 provider3=Catalog.provider3,
                                 provider4=Catalog.provider4)
assert Catalog.filter(Factory) == dict(provider1=Catalog.provider1,
                                       provider2=Catalog.provider2)
assert Catalog.filter(Singleton) == dict(provider3=Catalog.provider3,
                                         provider4=Catalog.provider4)
