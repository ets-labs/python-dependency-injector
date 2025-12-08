from typing import Any, Optional
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the return type
provider1 = providers.Delegate(providers.Provider())
var1 = provider1()
assert_type(var1, providers.Provider[Any])

# Test 2: to check the return type with await
provider2 = providers.Delegate(providers.Provider())


async def _async2() -> None:
    var1 = await provider2()  # type: ignore
    var2 = await provider2.async_()
    assert_type(var2, providers.Provider[Any])


# Test 3: to check class type from provider
provider3 = providers.Delegate(providers.Provider())
provided_provides = provider3.provides
assert_type(provided_provides, Optional[providers.Provider[Any]])
