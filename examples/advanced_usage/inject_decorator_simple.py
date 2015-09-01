"""`@di.inject` decorator simple example."""

import dependency_injector as di


dependency_injector_factory = di.Factory(object)


@di.inject(new_object=dependency_injector_factory)
@di.inject(some_setting=1334)
def example_callback(new_object, some_setting):
    """Example callback that does some asserts for input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334

example_callback()
