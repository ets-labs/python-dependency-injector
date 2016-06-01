"""Declarative IoC containers inheritance example."""

from dependency_injector import containers
from dependency_injector import providers


class ContainerA(containers.DeclarativeContainer):
    """Example IoC container A."""

    provider1 = providers.Factory(object)


class ContainerB(ContainerA):
    """Example IoC container B."""

    provider2 = providers.Singleton(object)


# Making some asserts for `providers` attribute:
assert ContainerA.providers == dict(provider1=ContainerA.provider1)
assert ContainerB.providers == dict(provider1=ContainerA.provider1,
                                    provider2=ContainerB.provider2)

# Making some asserts for `cls_providers` attribute:
assert ContainerA.cls_providers == dict(provider1=ContainerA.provider1)
assert ContainerB.cls_providers == dict(provider2=ContainerB.provider2)

# Making some asserts for `inherited_providers` attribute:
assert ContainerA.inherited_providers == dict()
assert ContainerB.inherited_providers == dict(provider1=ContainerB.provider1)
