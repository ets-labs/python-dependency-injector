import sys

if sys.version_info >= (3, 6):
    from dependency_injector.wiring import Provide

    from ..container import Container
    from ..service import Service


    def test_package_function(service: Service = Provide[Container.service]):
        return service
