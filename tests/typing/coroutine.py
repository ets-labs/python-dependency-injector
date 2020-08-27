from typing import Coroutine

from dependency_injector import providers


async def _coro() -> None:
    ...

# Test 1: to check the return type
provider1 = providers.Coroutine(_coro)
var1: Coroutine = provider1()
