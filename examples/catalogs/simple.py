"""Catalog  example."""

from collections import namedtuple

from objects.catalog import AbstractCatalog
from objects.providers import Factory
from objects.injections import KwArg


# Creating some example classes:
Object1 = namedtuple('Object1', ['arg1', 'arg2'])
Object2 = namedtuple('Object2', ['object1'])


class Catalog(AbstractCatalog):

    """Providers catalog."""

    object1_factory = Factory(Object1,
                              KwArg('arg1', 1),
                              KwArg('arg2', 2))
    """:type: (objects.Provider) -> Object1"""

    object2_factory = Factory(Object2,
                              KwArg('object1', object1_factory))
    """:type: (objects.Provider) -> Object2"""

# Creating some objects:
object2_1 = Catalog.object2_factory()
object2_2 = Catalog.object2_factory()

# Making some asserts:
assert object2_1 is not object2_2

assert isinstance(object2_1, Object2)
assert object2_1.object1.arg1 == 1
assert object2_1.object1.arg2 == 2

assert isinstance(object2_2, Object2)
assert object2_2.object1.arg1 == 1
assert object2_2.object1.arg2 == 2
