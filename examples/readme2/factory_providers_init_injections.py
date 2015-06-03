"""`Factory` providers with init injections example."""

from objects.providers import Factory
from objects.injections import KwArg


class A(object):

    """Example class A.

    Class A has dependencies on class B and class C objects, that have to be
    provided as init arguments.
    """

    def __init__(self, object_b, object_c):
        self.object_b = object_b
        self.object_c = object_c
        super(A, self).__init__()


class B(object):

    """Example class B."""


class C(object):

    """Example class C."""


# A, B, C factories:
c_factory = Factory(C)
b_factory = Factory(B)
a_factory = Factory(A,
                    KwArg('object_b', b_factory),
                    KwArg('object_c', c_factory))

# Creating several A objects:
object_a_1 = a_factory()  # Same as: A(object_b=B(), object_c=C())
object_a_2 = a_factory()  # Same as: A(object_b=B(), object_c=C())

# Making some asserts:
assert object_a_1 is not object_a_2
assert object_a_1.object_b is not object_a_2.object_b
assert object_a_1.object_c is not object_a_2.object_c
