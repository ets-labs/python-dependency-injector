"""`inject()` decorator simple example."""

import dependency_injector.providers as providers
import dependency_injector.injections as injections


dependency_injector_factory = providers.Factory(object)


# Example of using `inject()` decorator keyword argument injections:
@injections.inject(new_object=dependency_injector_factory)
@injections.inject(some_setting=1334)
def example_callback1(new_object, some_setting):
    """Example callback that does some asserts for input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334


# Example of using `inject()` decorator with positional argument injections:
@injections.inject(dependency_injector_factory, 1334)
def example_callback2(new_object, some_setting):
    """Example callback that does some asserts for input args."""
    assert isinstance(new_object, object)
    assert some_setting == 1334


example_callback1()
example_callback2()
