"""`Coroutine` providers example with @asyncio.coroutine decorator.

Current example works only fot Python 3.4+.
"""

import asyncio

import dependency_injector.providers as providers


@asyncio.coroutine
def coroutine_function(arg1, arg2):
    """Sample coroutine function."""
    yield from asyncio.sleep(0.1)
    return arg1, arg2


coroutine_provider = providers.Coroutine(coroutine_function, arg1=1, arg2=2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    arg1, arg2 = loop.run_until_complete(coroutine_provider())

    assert (arg1, arg2) == (1, 2)
    assert asyncio.iscoroutinefunction(coroutine_provider)
