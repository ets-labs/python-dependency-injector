from typing import Any

from dependency_injector import providers

# Test 1: to check the return type
provider1 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
var1: Any = provider1()

# Test 2: to check the provided instance interface
provider2 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
provided2: providers.ProvidedInstance = provider2.provided
attr_getter2: providers.AttributeGetter = provider2.provided.attr
item_getter2: providers.ItemGetter = provider2.provided["item"]
method_caller2: providers.MethodCaller = provider2.provided.method.call(123, arg=324)

# Test3 to check the getattr
provider3 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
attr3: providers.Provider[Any] = provider3.a

# Test 4: to check the return type with await
provider4 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)


async def _async4() -> None:
    var1: Any = await provider4()
    var2: Any = await provider4.async_()


# Test 5: to check explicit typing

provider5 = providers.Selector[bool](lambda: "a", a=providers.Factory(bool), b=providers.Factory(int))
var5: bool = provider5()
attr5: providers.Provider[Any] = provider5.a
provider5_after_set_selector: providers.Selector[bool] = provider5.set_selector(lambda: "a")
provider5_after_set_providers: providers.Selector[bool] = provider5.set_providers(
    c=providers.Factory(str)
) # We don't require Provider of subclass of bool yet since Provider is invariant