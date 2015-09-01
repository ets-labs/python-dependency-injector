"""Operating with catalog providers example."""

import dependency_injector as di


class Catalog(di.AbstractCatalog):

    """Providers catalog."""

    provider1 = di.Factory(object)
    """:type: (di.Provider) -> object"""

    provider2 = di.Factory(object)
    """:type: (di.Provider) -> object"""

    provider3 = di.Singleton(object)
    """:type: (di.Provider) -> object"""

    provider4 = di.Singleton(object)
    """:type: (di.Provider) -> object"""


# Making some asserts:
assert Catalog.providers == dict(provider1=Catalog.provider1,
                                 provider2=Catalog.provider2,
                                 provider3=Catalog.provider3,
                                 provider4=Catalog.provider4)
assert Catalog.filter(di.Factory) == dict(provider1=Catalog.provider1,
                                          provider2=Catalog.provider2)
assert Catalog.filter(di.Singleton) == dict(provider3=Catalog.provider3,
                                            provider4=Catalog.provider4)
