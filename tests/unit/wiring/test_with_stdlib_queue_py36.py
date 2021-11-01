"""Tests for wiring causes no issues with queue.Queue from std lib."""

from pytest import fixture

from samples.wiring import queuemodule
from samples.wiring.container import Container


@fixture
def container():
    container = Container()
    yield container
    container.unwire()


def test_wire_queue(container: Container):
    # See: https://github.com/ets-labs/python-dependency-injector/issues/362
    # Should not raise exception
    try:
        container.wire(modules=[queuemodule])
    except:
        raise
