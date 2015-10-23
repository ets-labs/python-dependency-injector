"""`@di.inject()` decorator simple example."""

import dependency_injector as di


dependency_injector_factory = di.Factory(object)


# Example of using `di.inject()` decorator keyword argument injections:
@di.inject(new_object=dependency_injector_factory)
@di.inject(some_setting=1334)
def example_callback1(new_object, some_setting):
    """Example callback that does some asserts for input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334


# Example of using `di.inject()` decorator with positional argument injections:
@di.inject(dependency_injector_factory, 1334)
def example_callback2(new_object, some_setting):
    """Example callback that does some asserts for input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334


example_callback1()
example_callback2()
