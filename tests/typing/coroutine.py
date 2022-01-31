from typing import Coroutine

from dependency_injector import providers


async def _coro() -> None:
    ...

# Test 1: to check the return type
provider1 = providers.Coroutine(_coro)
var1: Coroutine = provider1()

# Test 2: to check string imports
provider2: providers.Coroutine[None] = providers.Coroutine("_coro")
provider2.set_provides("_coro")
