from dependency_injector.wiring import inject, Provide

from ...container import Container
from ...service import Service


@inject
def test_function(service: Service = Provide[Container.service]):
    return service
