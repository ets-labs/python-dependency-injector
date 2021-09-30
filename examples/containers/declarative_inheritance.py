"""Declarative containers inheritance example."""

from dependency_injector import containers, providers


class ContainerA(containers.DeclarativeContainer):

    provider1 = providers.Factory(object)


class ContainerB(ContainerA):

    provider2 = providers.Singleton(object)


assert ContainerA.providers == {
    "provider1": ContainerA.provider1,
}
assert ContainerB.providers == {
    "provider1": ContainerA.provider1,
    "provider2": ContainerB.provider2,
}

assert ContainerA.cls_providers == {
    "provider1": ContainerA.provider1,
}
assert ContainerB.cls_providers == {
    "provider2": ContainerB.provider2,
}

assert ContainerA.inherited_providers == {}
assert ContainerB.inherited_providers == {
    "provider1": ContainerA.provider1,
}
