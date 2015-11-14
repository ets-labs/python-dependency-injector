"""Declarative catalog API example."""

from dependency_injector import catalogs
from dependency_injector import providers


class CatalogA(catalogs.DeclarativeCatalog):
    """Example catalog A."""

    provider1 = providers.Factory(object)
    """:type: providers.Provider -> object"""


class CatalogB(CatalogA):
    """Example catalog B."""

    provider2 = providers.Singleton(object)
    """:type: providers.Provider -> object"""


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
