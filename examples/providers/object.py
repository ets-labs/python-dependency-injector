"""Object providers example."""

import dependency_injector.providers as providers


# Creating object provider:
object_provider = providers.Object(1)

# Making some asserts:
assert object_provider() == 1
