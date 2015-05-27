"""`Factory` providers with constructor injections example."""

from objects.providers import Factory
from objects.injections import KwArg


class ObjectA(object):

    """ObjectA has few dependencies that need to provided as init args."""

    def __init__(self, object_b, object_c):
        """Initializer."""
        self.object_b = object_b
        self.object_c = object_c


# Creating of dependencies.
object_b = object()
object_c = object()

# Creating ObjectA factory.
object_a_factory = Factory(ObjectA,
                           KwArg('object_b', object_b),
                           KwArg('object_c', object_c))


object_a_1 = object_a_factory()  # Same as ObjectA(object_b, object_c)
object_a_2 = object_a_factory()  # Same as ObjectA(object_b, object_c)

assert object_a_1 is not object_a_2
assert isinstance(object_a_1, ObjectA)
assert isinstance(object_a_2, ObjectA)
assert object_a_1.object_b is object_a_2.object_b is object_b
assert object_a_1.object_c is object_a_2.object_c is object_c
