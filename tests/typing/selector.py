from typing import Any, Callable, Optional, Dict

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


# Test 5: to check selector getter and setter
provider5 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
selector5: Optional[Callable[..., Any]] = provider5.selector
provider5_after_set_selector: providers.Selector[Any] = provider5.set_selector(lambda: "a")

# Test 6: to check providers getter and setter
provider6 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
providers6: Dict[str, providers.Provider[Any]] = provider6.providers
provider6_after_set_providers: providers.Selector[Any] = provider6.set_providers(c=providers.Factory(object))


# Test 7: to check explicit typing: return type, getattr, getter/setter of providers and selectors
provider7 = providers.Selector[bool](lambda: "a", a=providers.Factory(bool), b=providers.Factory(int))
var7: bool = provider7()
attr7: providers.Provider[bool] = provider7.a

selector7: Optional[Callable[..., Any]] = provider7.selector
provider7_after_set_selector: providers.Selector[bool] = provider7.set_selector(lambda: "a")

providers7: Dict[str, providers.Provider[bool]] = provider7.providers
provider7_after_set_providers: providers.Selector[bool] = provider7.set_providers(
    c=providers.Factory(str)
)  # We don't require Provider of subclass of bool yet since Provider is invariant
