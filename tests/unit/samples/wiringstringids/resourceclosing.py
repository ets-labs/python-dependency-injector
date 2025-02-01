from typing import Any, Dict, List, Optional

from dependency_injector import containers, providers
from dependency_injector.wiring import Closing, Provide, inject


class Counter:
    def __init__(self) -> None:
        self._init = 0
        self._shutdown = 0

    def init(self) -> None:
        self._init += 1

    def shutdown(self) -> None:
        self._shutdown += 1

    def reset(self) -> None:
        self._init = 0
        self._shutdown = 0


class Service:
    def __init__(self, counter: Optional[Counter] = None, **dependencies: Any) -> None:
        self.counter = counter or Counter()
        self.dependencies = dependencies

    def init(self) -> None:
        self.counter.init()

    def shutdown(self) -> None:
        self.counter.shutdown()

    @property
    def init_counter(self) -> int:
        return self.counter._init

    @property
    def shutdown_counter(self) -> int:
        return self.counter._shutdown


class FactoryService:
    def __init__(self, service: Service, service2: Service):
        self.service = service
        self.service2 = service2


class NestedService:
    def __init__(self, factory_service: FactoryService):
        self.factory_service = factory_service


def init_service(counter: Counter, _list: List[int], _dict: Dict[str, int]):
    service = Service(counter, _list=_list, _dict=_dict)
    service.init()
    yield service
    service.shutdown()


class Container(containers.DeclarativeContainer):
    counter = providers.Singleton(Counter)
    _list = providers.List(
        providers.Callable(lambda a: a, a=1), providers.Callable(lambda b: b, 2)
    )
    _dict = providers.Dict(
        a=providers.Callable(lambda a: a, a=3), b=providers.Callable(lambda b: b, 4)
    )
    service = providers.Resource(init_service, counter, _list, _dict=_dict)
    service2 = providers.Resource(init_service, counter, _list, _dict=_dict)
    factory_service = providers.Factory(FactoryService, service, service2)
    factory_service_kwargs = providers.Factory(
        FactoryService,
        service=service,
        service2=service2,
    )
    nested_service = providers.Factory(NestedService, factory_service)


@inject
def test_function(service: Service = Closing[Provide["service"]]):
    return service


@inject
def test_function_dependency(
    factory: FactoryService = Closing[Provide["factory_service"]],
):
    return factory


@inject
def test_function_dependency_kwargs(
    factory: FactoryService = Closing[Provide["factory_service_kwargs"]],
):
    return factory


@inject
def test_function_nested_dependency(
    nested: NestedService = Closing[Provide["nested_service"]],
):
    return nested
