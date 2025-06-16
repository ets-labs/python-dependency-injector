from wiringfastdepends import sample


def test_apply_coefficient() -> None:
    assert sample.apply_coefficient(100) == 120.0


def test_apply_coefficient_annotated() -> None:
    assert sample.apply_coefficient_annotated(100) == 120.0
