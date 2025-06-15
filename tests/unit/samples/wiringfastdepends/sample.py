from dependency_injector.wiring import inject, Provide
from fast_depends import Depends

# Runtime import to avoid syntax errors in samples on Python < 3.5 and reach top-dir
import os

_SAMPLES_DIR = os.path.abspath(
    os.path.sep.join(
        (
            os.path.dirname(__file__),
            "../samples/",
        )
    ),
)
import sys

sys.path.append(_SAMPLES_DIR)


from wiringfastdepends.sample import CoefficientService, Container



@inject
def apply_coefficient(
    a: int,
    coefficient_provider: CoefficientService = Depends(Provide[Container.service]),
) -> float:
    return a * coefficient_provider.get_coefficient()


container = Container()
container.wire(modules=[sys.modules[__name__]])


def test_wire_positive() -> None:
    assert apply_coefficient(100) == 120.0