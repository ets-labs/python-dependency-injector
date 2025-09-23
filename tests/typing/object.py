from typing import Optional, Type

from dependency_injector import providers

# Test 1: to check the return type
provider1 = providers.Object(int(3))
var1: int = provider1()

# Test 2: to check the provided instance interface
provider2 = providers.Object(int)
provided2: Type[int] = provider2.provided()
attr_getter2: providers.AttributeGetter = provider2.provided.attr
item_getter2: providers.ItemGetter = provider2.provided["item"]
method_caller2: providers.MethodCaller = provider2.provided.method.call(123, arg=324)

# Test 3: to check the return type with await
provider3 = providers.Object(int(3))


async def _async3() -> None:
    var1: int = await provider3()  # type: ignore
    var2: int = await provider3.async_()


# Test 4: to check class type from provider
provider4 = providers.Object(int("1"))
provided_provides: Optional[int] = provider4.provides
