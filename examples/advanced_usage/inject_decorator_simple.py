"""`@inject` decorator simple example."""

from dependency_injector.providers import Factory
from dependency_injector.injections import KwArg
from dependency_injector.injections import inject


dependency_injector_factory = Factory(object)


@inject(KwArg('new_object', dependency_injector_factory))
@inject(KwArg('some_setting', 1334))
def example_callback(new_object, some_setting):
    """Example callback that does some asserts with input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334

example_callback()
