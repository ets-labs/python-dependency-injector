from typing import Tuple, Any, List

from dependency_injector import providers


# Test 1: to check the return type (class)
provider1 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
var1: List[Any] = provider1()


# Test 2: to check the .args attributes
provider2 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
args2: Tuple[Any] = provider2.args

# Test 3: to check the provided instance interface
provider3 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
provided3: providers.ProvidedInstance = provider3.provided
attr_getter3: providers.AttributeGetter = provider3.provided.attr
item_getter3: providers.ItemGetter = provider3.provided['item']
method_caller3: providers.MethodCaller = provider3.provided.method.call(123, arg=324)

# Test 4: to check the return type with await
provider4 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
async def _async4() -> None:
    var1: List[Any] = await provider4()  # type: ignore
    var2: List[Any] = await provider4.async_()
