from typing import Any, Dict

from dependency_injector import providers


# Test 1: to check the return type (class)
provider1 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
var1: Dict[Any, Any] = provider1()


# Test 2: to check init with non-string keys
provider2 = providers.Dict({object(): providers.Factory(object)})
var2: Dict[Any, Any] = provider2()


# Test 3: to check init with non-string keys
provider3 = providers.Dict({object(): providers.Factory(object)}, a2=providers.Factory(object))
var3: Dict[Any, Any] = provider3()


# Test 4: to check the .args attributes
provider4 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
args4: Dict[Any, Any] = provider4.kwargs


# Test 5: to check the provided instance interface
provider5 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
provided5: providers.ProvidedInstance = provider5.provided


# Test 6: to check the return type with await
provider6 = providers.Dict(
    a1=providers.Factory(object),
    a2=providers.Factory(object),
)
async def _async3() -> None:
    var1: Dict[Any, Any] = await provider6()  # type: ignore
    var2: Dict[Any, Any] = await provider6.async_()
