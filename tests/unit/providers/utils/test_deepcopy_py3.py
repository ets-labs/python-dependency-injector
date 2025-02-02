import sys
from typing import Any, Dict, NoReturn

from pytest import raises

from dependency_injector.errors import NonCopyableArgumentError
from dependency_injector.providers import (
    Provider,
    deepcopy,
    deepcopy_args,
    deepcopy_kwargs,
)


class NonCopiable:
    def __deepcopy__(self, memo: Dict[int, Any]) -> NoReturn:
        raise NotImplementedError


def test_deepcopy_streams_not_copied() -> None:
    l = [sys.stdin, sys.stdout, sys.stderr]
    assert deepcopy(l) == l


def test_deepcopy_args() -> None:
    provider = Provider[None]()
    copiable = NonCopiable()
    memo: Dict[int, Any] = {id(copiable): copiable}

    assert deepcopy_args(provider, (1, copiable), memo) == (1, copiable)


def test_deepcopy_args_non_copiable() -> None:
    provider = Provider[None]()
    copiable = NonCopiable()
    memo: Dict[int, Any] = {id(copiable): copiable}

    with raises(
        NonCopyableArgumentError,
        match=r"^Couldn't copy argument at index 3 for provider ",
    ):
        deepcopy_args(provider, (1, copiable, object(), NonCopiable()), memo)


def test_deepcopy_kwargs() -> None:
    provider = Provider[None]()
    copiable = NonCopiable()
    memo: Dict[int, Any] = {id(copiable): copiable}

    assert deepcopy_kwargs(provider, {"x": 1, "y": copiable}, memo) == {
        "x": 1,
        "y": copiable,
    }


def test_deepcopy_kwargs_non_copiable() -> None:
    provider = Provider[None]()
    copiable = NonCopiable()
    memo: Dict[int, Any] = {id(copiable): copiable}

    with raises(
        NonCopyableArgumentError,
        match=r"^Couldn't copy keyword argument z for provider ",
    ):
        deepcopy_kwargs(provider, {"x": 1, "y": copiable, "z": NonCopiable()}, memo)
