from typing import Any, Callable, Dict, Optional, Tuple
from typing_extensions import assert_type

from dependency_injector import providers


class Animal: ...


class Cat(Animal):
    @classmethod
    def create(cls) -> Animal:
        return cls()


# Test 1: to check the return type (class)
provider1 = providers.Callable(Cat)
cat1 = provider1(1, 2, 3, b="1", c=2, e=0.0)
assert_type(cat1, Cat)

# Test 2: to check the return type (class factory method)
provider2 = providers.Callable(Cat.create)
animal2 = provider2()
assert_type(animal2, Animal)

# Test 3: to check the .override() method
provider3 = providers.Callable(Animal)
with provider3.override(providers.Callable(Cat)):
    provider3()

# Test 4: to check the .args & .kwargs attributes
provider4 = providers.Callable(Animal)
args4 = provider4.args
kwargs4 = provider4.kwargs
assert_type(args4, Tuple[Any])
assert_type(kwargs4, Dict[str, Any])

# Test 5: to check the provided instance interface
provider5 = providers.Callable(Animal)
provided_val5 = provider5.provided()
attr_getter5 = provider5.provided.attr
item_getter5 = provider5.provided["item"]
method_caller5 = provider5.provided.method.call(123, arg=324)
assert_type(provided_val5, Any)
assert_type(attr_getter5, providers.AttributeGetter)
assert_type(item_getter5, providers.ItemGetter)
assert_type(method_caller5, providers.MethodCaller)

# Test 6: to check the DelegatedCallable
provider6 = providers.DelegatedCallable(Cat)
cat6 = provider6(1, 2, 3, b="1", c=2, e=0.0)
assert_type(cat6, Cat)

# Test 7: to check the AbstractCallable
provider7 = providers.AbstractCallable(Animal)
provider7.override(providers.Callable(Cat))
animal7 = provider7(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal7, Animal)

# Test 8: to check the CallableDelegate __init__
provider8 = providers.CallableDelegate(providers.Callable(lambda: None))

# Test 9: to check the return type with await
provider9 = providers.Callable(Cat)


async def _async9() -> None:
    await provider9(1, 2, 3, b="1", c=2, e=0.0)  # type: ignore[misc]
    cat9 = await provider9.async_(1, 2, 3, b="1", c=2, e=0.0)
    assert_type(cat9, Cat)


# Test 10: to check the .provides
provider10 = providers.Callable(Cat)
provides10 = provider10.provides
assert_type(provides10, Optional[Callable[..., Cat]])

# Test 11: to check the .provides for explicit typevar
provider11 = providers.Callable[Animal](Cat)
provides11 = provider11.provides
assert_type(provides11, Optional[Callable[..., Animal]])


# Test 12: to check string imports
provider12 = providers.Callable("builtins.dict")
provider12.set_provides("builtins.dict")
