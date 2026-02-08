from typing import Any, List, Tuple
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the return type (class)
provider1 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
var1 = provider1()
assert_type(var1, List[Any])


# Test 2: to check the .args attributes
provider2 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
args2 = provider2.args
assert_type(args2, Tuple[Any])

# Test 3: to check the provided instance interface
provider3 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)
provided3 = provider3.provided
provided_val3 = provided3()
attr_getter3 = provider3.provided.attr
item_getter3 = provider3.provided["item"]
method_caller3 = provider3.provided.method.call(123, arg=324)
assert_type(provided3, providers.ProvidedInstance)
assert_type(provided_val3, Any)
assert_type(attr_getter3, providers.AttributeGetter)
assert_type(item_getter3, providers.ItemGetter)
assert_type(method_caller3, providers.MethodCaller)

# Test 4: to check the return type with await
provider4 = providers.List(
    providers.Factory(object),
    providers.Factory(object),
)


async def _async4() -> None:
    var1 = await provider4()  # type: ignore
    var2 = await provider4.async_()
    assert_type(var2, List[Any])
