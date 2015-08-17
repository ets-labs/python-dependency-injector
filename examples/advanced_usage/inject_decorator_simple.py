"""`@inject` decorator simple example."""

from objects.providers import Factory
from objects.injections import KwArg
from objects.injections import inject


objects_factory = Factory(object)


@inject(KwArg('new_object', objects_factory))
@inject(KwArg('some_setting', 1334))
def example_callback(new_object, some_setting):
    """Example callback that does some asserts with input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334

example_callback()
