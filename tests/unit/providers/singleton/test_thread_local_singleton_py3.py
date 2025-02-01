import pytest

from dependency_injector.containers import Container
from dependency_injector.providers import ThreadLocalSingleton


class FailingClass:
    def __init__(self):
        raise ValueError("FAILING CLASS")


class TestContainer(Container):
    failing_class = ThreadLocalSingleton(FailingClass)


def test_on_failure_value_error_is_raised():
    container = TestContainer()

    with pytest.raises(ValueError, match="FAILING CLASS"):
        container.failing_class()
