from typing import Any, Dict
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the return type (class)
provider1 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
var1 = provider1()
assert_type(var1, Dict[Any, Any])


# Test 2: to check init with non-string keys
provider2 = providers.Dict({object(): providers.Factory(object)})
var2 = provider2()
assert_type(var2, Dict[Any, Any])


# Test 3: to check init with non-string keys
provider3 = providers.Dict(
    {object(): providers.Factory(object)}, a2=providers.Factory(object)
)
var3 = provider3()
assert_type(var3, Dict[Any, Any])


# Test 4: to check the .args attributes
provider4 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
args = provider4.kwargs
assert_type(args, Dict[Any, Any])


# Test 5: to check the provided instance interface
provider5 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
provided5 = provider5.provided()
assert_type(provided5, Any)


# Test 6: to check the return type with await
provider6 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)


async def _async3() -> None:
    var1 = await provider6()  # type: ignore
    var2 = await provider6.async_()
    assert_type(var2, Dict[Any, Any])
