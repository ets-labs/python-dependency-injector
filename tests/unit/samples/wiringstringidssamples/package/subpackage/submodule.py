from dependency_injector.wiring import inject, Provide

from ...service import Service


@inject
def test_function(service: Service = Provide['service']):
    return service
