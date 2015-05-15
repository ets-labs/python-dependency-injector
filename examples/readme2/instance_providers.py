"""`Factory` and `Singleton` providers example."""

from objects.providers import Factory
from objects.providers import Singleton


# Factory provider creates new instance of specified class on every call.
object_factory = Factory(object)

object_1 = object_factory()
object_2 = object_factory()

assert object_1 is not object_2
assert isinstance(object_1, object) and isinstance(object_2, object)

# Singleton provider creates new instance of specified class on first call
# and returns same instance on every next call.
single_object = Singleton(object)

single_object_1 = single_object()
single_object_2 = single_object()

assert single_object_1 is single_object_2
assert isinstance(object_1, object) and isinstance(object_2, object)
