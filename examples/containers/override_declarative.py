"""Declarative IoC container overriding example."""

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Container(containers.DeclarativeContainer):
    """IoC container."""

    sequence_factory = providers.Factory(list)


class OverridingContainer(containers.DeclarativeContainer):
    """Overriding IoC container."""

    sequence_factory = providers.Factory(tuple)


# Overriding `Container` with `OverridingContainer`:
Container.override(OverridingContainer)

# Creating some objects using overridden container:
sequence_1 = Container.sequence_factory([1, 2, 3])
sequence_2 = Container.sequence_factory([3, 2, 1])

# Making some asserts:
assert Container.overridden == (OverridingContainer,)
assert sequence_1 == (1, 2, 3) and sequence_2 == (3, 2, 1)
