"""`Factory` providers example."""

from objects.providers import Factory


# Factory provider creates new instance of specified class on every call.
object_factory = Factory(object)

object_1 = object_factory()
object_2 = object_factory()

assert object_1 is not object_2
assert isinstance(object_1, object) and isinstance(object_2, object)
