"""`Coroutine` providers example with async / await syntax."""

import asyncio

from dependency_injector import containers, providers


async def coroutine(arg1, arg2):
    await asyncio.sleep(0.1)
    return arg1, arg2


class Container(containers.DeclarativeContainer):

    coroutine_provider = providers.Coroutine(coroutine, arg1=1, arg2=2)


if __name__ == "__main__":
    container = Container()

    arg1, arg2 = asyncio.run(container.coroutine_provider())
    assert (arg1, arg2) == (1, 2)
    assert asyncio.iscoroutinefunction(container.coroutine_provider)
