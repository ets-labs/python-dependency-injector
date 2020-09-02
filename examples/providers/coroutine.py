"""`Coroutine` providers example with async / await syntax."""

import asyncio

from dependency_injector import providers


async def coroutine(arg1, arg2):
    await asyncio.sleep(0.1)
    return arg1, arg2


coroutine_provider = providers.Coroutine(coroutine, arg1=1, arg2=2)


if __name__ == '__main__':
    arg1, arg2 = asyncio.run(coroutine_provider())
    assert (arg1, arg2) == (1, 2)
    assert asyncio.iscoroutinefunction(coroutine_provider)
