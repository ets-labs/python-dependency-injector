"""Test that wiring skips classmethods wrapping non-callable descriptors.

See issue for details: https://github.com/ets-labs/python-dependency-injector/issues/950
"""

import sys
from functools import singledispatchmethod

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class Container(DeclarativeContainer):
    singleton = providers.Singleton(lambda: object())


class Model:
    @classmethod
    @singledispatchmethod
    def validate(cls, param):
        return param


def test_wire_classmethod_wrapping_singledispatchmethod():
    descriptor = Model.__dict__["validate"]

    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    try:
        assert Model.__dict__["validate"] is descriptor
    finally:
        container.unwire()
