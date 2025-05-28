"""Tests for string module and package names."""

from typing import Iterator, Optional

from pytest import fixture, mark
from samples.wiring.container import Container

from dependency_injector.wiring import _fetch_reference_injections


@fixture
def container() -> Iterator[Container]:
    container = Container()
    yield container
    container.unwire()


@mark.parametrize(
    ["arg_value", "wc_value", "empty_cache"],
    [
        (None, False, True),
        (False, True, True),
        (True, False, False),
        (None, True, False),
    ],
)
def test_fetch_reference_injections_cache(
    container: Container,
    arg_value: Optional[bool],
    wc_value: bool,
    empty_cache: bool,
) -> None:
    container.wiring_config.keep_cache = wc_value
    container.wire(
        modules=["samples.wiring.module"],
        packages=["samples.wiring.package"],
        keep_cache=arg_value,
    )
    cache_info = _fetch_reference_injections.cache_info()

    if empty_cache:
        assert cache_info == (0, 0, None, 0)
    else:
        assert cache_info.hits > 0
        assert cache_info.misses > 0
        assert cache_info.currsize > 0
