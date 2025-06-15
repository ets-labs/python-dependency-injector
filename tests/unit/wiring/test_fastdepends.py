from dependency_injector.wiring import inject, Provide

from wiringfastdepends import sample


def test_apply_coefficient():
    assert sample.apply_coefficient(100) == 120.0