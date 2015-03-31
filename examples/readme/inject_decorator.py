"""`@inject` decorator example."""

from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import inject


object_a = NewInstance(object)
object_b = NewInstance(object)


@inject(KwArg('a', object_a))
@inject(KwArg('b', object_b))
def example_callback(a, b):
    """This function has dependencies on object a and b.

    Dependencies are injected using `@inject` decorator.
    """
    assert a is not b
    assert isinstance(a, object)
    assert isinstance(b, object)


example_callback()
