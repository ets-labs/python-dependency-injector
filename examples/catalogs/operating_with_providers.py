"""Operating with catalog providers example."""

import dependency_injector as di


class CatalogA(di.AbstractCatalog):

    """Example catalog A."""

    provider1 = di.Factory(object)
    """:type: (di.Provider) -> object"""


class CatalogB(CatalogA):

    """Example catalog B."""

    provider2 = di.Singleton(object)
    """:type: (di.Provider) -> object"""


# Making some asserts for `providers` attribute:
assert CatalogA.providers == dict(provider1=CatalogA.provider1)
assert CatalogB.providers == dict(provider1=CatalogA.provider1,
                                  provider2=CatalogB.provider2)

# Making some asserts for `cls_providers` attribute:
assert CatalogA.cls_providers == dict(provider1=CatalogA.provider1)
assert CatalogB.cls_providers == dict(provider2=CatalogB.provider2)

# Making some asserts for `inherited_providers` attribute:
assert CatalogA.inherited_providers == dict()
assert CatalogB.inherited_providers == dict(provider1=CatalogA.provider1)

# Making some asserts for `filter()` method:
assert CatalogB.filter(di.Factory) == dict(provider1=CatalogA.provider1)
assert CatalogB.filter(di.Singleton) == dict(provider2=CatalogB.provider2)
