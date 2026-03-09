from typing import Optional, Any
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the return type
provider1 = providers.Object(int(3))
var1 = provider1()
assert_type(var1, int)

# Test 2: to check the provided instance interface
provider2 = providers.Object(int)
provided2 = provider2.provided
provided_val2 = provided2()
attr_getter2 = provider2.provided.attr
item_getter2 = provider2.provided["item"]
method_caller2 = provider2.provided.method.call(123, arg=324)
assert_type(provided2, providers.ProvidedInstance)
assert_type(provided_val2, Any)
assert_type(attr_getter2, providers.AttributeGetter)
assert_type(item_getter2, providers.ItemGetter)
assert_type(method_caller2, providers.MethodCaller)


# Test 3: to check the return type with await
provider3 = providers.Object(int(3))


async def _async3() -> None:
    var1 = await provider3()  # type: ignore
    var2 = await provider3.async_()
    assert_type(var2, int)


# Test 4: to check class type from provider
provider4 = providers.Object(int("1"))
provided_provides4 = provider4.provides
assert_type(provided_provides4, Optional[int])
