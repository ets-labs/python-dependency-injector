from typing import Any, Callable, Optional, Dict
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the return type
provider1 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
var1 = provider1()
assert_type(var1, Any)

# Test 2: to check the provided instance interface
provider2 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
provided2 = provider2.provided
provided_val2 = provided2()
attr_getter2 = provider2.provided.attr
item_getter2 = provider2.provided["item"]
method_caller2 = provider2.provided.method.call(123, arg=324)
assert_type(provider2, providers.Selector[Any])
assert_type(provided2, providers.ProvidedInstance)
assert_type(provided_val2, Any)
assert_type(attr_getter2, providers.AttributeGetter)
assert_type(item_getter2, providers.ItemGetter)
assert_type(method_caller2, providers.MethodCaller)

# Test3 to check the getattr
provider3 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
attr3 = provider3.a
assert_type(attr3, providers.Provider[Any])

# Test 4: to check the return type with await
provider4 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)


async def _async4() -> None:
    var1 = await provider4()
    var2 = await provider4.async_()
    assert_type(var1, Any)
    assert_type(var2, Any)


# Test 5: to check selector getter and setter
provider5 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
selector5 = provider5.selector
provider5_after_set_selector = provider5.set_selector(lambda: "a")
assert_type(selector5, Optional[Callable[..., Any]])
assert_type(provider5_after_set_selector, providers.Selector[Any])

# Test 6: to check providers getter and setter
provider6 = providers.Selector(
    lambda: "a",
    a=providers.Factory(object),
    b=providers.Factory(object),
)
providers6 = provider6.providers
provider6_after_set_providers = provider6.set_providers(c=providers.Factory(object))
assert_type(providers6, Dict[str, providers.Provider[Any]])
assert_type(provider6_after_set_providers, providers.Selector[Any])

# Test 7: to check explicit typing: return type, getattr, getter/setter of providers and selectors
provider7 = providers.Selector[bool](
    lambda: "a", a=providers.Factory(bool), b=providers.Factory(int)
)
var7 = provider7()
attr7 = provider7.a
assert_type(var7, bool)
assert_type(attr7, providers.Provider[bool])

selector7 = provider7.selector
provider7_after_set_selector = provider7.set_selector(lambda: "a")
assert_type(selector7, Optional[Callable[..., Any]])
assert_type(provider7_after_set_selector, providers.Selector[bool])

providers7 = provider7.providers
provider7_after_set_providers = provider7.set_providers(
    c=providers.Factory(str)
)  # We don't require Provider of subclass of bool yet since Provider is invariant
assert_type(providers7, Dict[str, providers.Provider[bool]])
assert_type(provider7_after_set_providers, providers.Selector[bool])
