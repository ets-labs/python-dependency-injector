"""Dynamic container simple example."""

import dependency_injector.containers as containers
import dependency_injector.providers as providers


# Defining dynamic container:
container = containers.DynamicContainer()
container.factory1 = providers.Factory(object)
container.factory2 = providers.Factory(object)

# Creating some objects:
object1 = container.factory1()
object2 = container.factory2()

# Making some asserts:
assert object1 is not object2
assert isinstance(object1, object) and isinstance(object2, object)
