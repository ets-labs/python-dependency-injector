import sys

from fast_depends import Depends
from typing_extensions import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class CoefficientService:
    @staticmethod
    def get_coefficient() -> float:
        return 1.2


class Container(containers.DeclarativeContainer):
    service = providers.Factory(CoefficientService)


@inject
def apply_coefficient(
    a: int,
    coefficient_provider: CoefficientService = Depends(Provide[Container.service]),
) -> float:
    return a * coefficient_provider.get_coefficient()


@inject
def apply_coefficient_annotated(
    a: int,
    coefficient_provider: Annotated[
        CoefficientService, Depends(Provide[Container.service])
    ],
) -> float:
    return a * coefficient_provider.get_coefficient()


container = Container()
container.wire(modules=[sys.modules[__name__]])
