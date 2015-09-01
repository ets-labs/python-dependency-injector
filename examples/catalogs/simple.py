"""Catalog example."""

import collections
import dependency_injector as di


# Creating some example classes:
Object1 = collections.namedtuple('Object1', ['arg1', 'arg2'])
Object2 = collections.namedtuple('Object2', ['object1'])


class Catalog(di.AbstractCatalog):

    """Providers catalog."""

    object1_factory = di.Factory(Object1,
                                 arg1=1,
                                 arg2=2)
    """:type: (di.Provider) -> Object1"""

    object2_factory = di.Factory(Object2,
                                 object1=object1_factory)
    """:type: (di.Provider) -> Object2"""

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
