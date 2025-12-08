from typing import Awaitable, Coroutine, Any
from typing_extensions import assert_type

from dependency_injector import providers


async def _coro() -> None: ...


# Test 1: to check the return type
provider1 = providers.Coroutine(_coro)
var1 = provider1()
assert_type(var1, Coroutine[Any, Any, None])  # type: ignore[unused-coroutine]

# Test 2: to check string imports
provider2 = providers.Coroutine("_coro")
provider2.set_provides("_coro")
assert_type(provider2, providers.Coroutine[Any])
