"""Declarative IoC container overriding example."""

import collections

from dependency_injector import containers
from dependency_injector import providers


# Creating some example classes:
Object1 = collections.namedtuple('Object1', ['arg1', 'arg2'])
Object2 = collections.namedtuple('Object2', ['object1'])
ExtendedObject2 = collections.namedtuple('ExtendedObject2', [])


class Container(containers.DeclarativeContainer):
    """Example IoC container."""

    object1_factory = providers.Factory(Object1,
                                        arg1=1,
                                        arg2=2)

    object2_factory = providers.Factory(Object2,
                                        object1=object1_factory)


class OverridingContainer(containers.DeclarativeContainer):
    """Overriding IoC container."""

    object2_factory = providers.Factory(ExtendedObject2)


# Overriding `Container` with `OverridingContainer`:
Container.override(OverridingContainer)

# Creating some objects using overridden container:
object2_1 = Container.object2_factory()
object2_2 = Container.object2_factory()

# Making some asserts:
assert Container.overridden_by == (OverridingContainer,)

assert object2_1 is not object2_2

assert isinstance(object2_1, ExtendedObject2)
assert isinstance(object2_2, ExtendedObject2)
