# cython: language_level=3, binding=True, embedsignature=True, annotation_typing=False

from dependency_injector.wiring import Provide

from samples.wiringcython.container import Container, Service


def sync_handler(svc: Service = Provide[Container.service]) -> str:
    return svc.get()


async def async_handler(svc: Service = Provide[Container.service]) -> str:
    return await svc.aget()


async def async_gen_handler(svc: Service = Provide[Container.service]):
    yield svc.get()
    yield svc.get() + "_2"


class HandlerClass:
    async def __call__(self, svc: Service = Provide[Container.service]) -> str:
        return svc.get()
