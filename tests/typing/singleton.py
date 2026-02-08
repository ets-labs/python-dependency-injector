from typing import Any, Callable, Dict, Optional, Tuple, Type
from typing_extensions import assert_type

from dependency_injector import providers


class Animal: ...


class Cat(Animal):

    def __init__(self, *a: Any, **kw: Any) -> None: ...

    @classmethod
    def create(cls) -> Animal:
        return cls()


# Test 1: to check the return type (class)
provider1 = providers.Singleton(Cat)
animal1 = provider1(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal1, Cat)

# Test 2: to check the return type (class factory method)
provider2 = providers.Singleton(Cat.create)
animal2 = provider2()
assert_type(animal2, Animal)

# Test 3: to check the .override() method
provider3 = providers.Singleton(Animal)
with provider3.override(providers.Singleton(Cat)):
    animal3 = provider3()
    assert_type(animal3, Animal)

# Test 4: to check the .args, .kwargs, .attributes attributes
provider4 = providers.Singleton(Animal)
args4 = provider4.args
kwargs4 = provider4.kwargs
attributes4 = provider4.attributes
assert_type(args4, Tuple[Any])
assert_type(kwargs4, Dict[str, Any])
assert_type(attributes4, Dict[str, Any])

# Test 5: to check the provided instance interface
provider5 = providers.Singleton(Animal)
provided5 = provider5.provided
provided_val5 = provided5()
attr_getter5 = provider5.provided.attr
item_getter5 = provider5.provided["item"]
method_caller5 = provider5.provided.method.call(123, arg=324)
assert_type(provided5, providers.ProvidedInstance)
assert_type(provided_val5, Any)
assert_type(attr_getter5, providers.AttributeGetter)
assert_type(item_getter5, providers.ItemGetter)
assert_type(method_caller5, providers.MethodCaller)

# Test 6: to check the DelegatedSingleton
provider6 = providers.DelegatedSingleton(Cat)
animal6 = provider6(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal6, Cat)

# Test 7: to check the ThreadSafeSingleton
provider7 = providers.ThreadSafeSingleton(Cat)
animal7 = provider7()
assert_type(animal7, Cat)

# Test 8: to check the DelegatedThreadSafeSingleton
provider8 = providers.DelegatedThreadSafeSingleton(Cat)
animal8 = provider8(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal8, Cat)

# Test 9: to check the ThreadLocalSingleton
provider9 = providers.ThreadLocalSingleton(Cat)
animal9 = provider9(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal9, Cat)

# Test 10: to check the DelegatedThreadLocalSingleton
provider10 = providers.DelegatedThreadLocalSingleton(Cat)
animal10 = provider10(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal10, Cat)

# Test 11: to check the AbstractSingleton
provider11 = providers.AbstractSingleton(Animal)
provider11.override(providers.Singleton(Cat))
animal11 = provider11(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal11, Animal)

# Test 12: to check the SingletonDelegate __init__
provider12 = providers.SingletonDelegate(providers.Singleton(object))

# Test 13: to check the return type with await
provider13 = providers.Singleton(Cat)


async def _async13() -> None:
    animal1 = await provider13(1, 2, 3, b="1", c=2, e=0.0)  # type: ignore
    animal2 = await provider13.async_(1, 2, 3, b="1", c=2, e=0.0)
    assert_type(animal2, Cat)


# Test 14: to check class from .provides
provider14 = providers.Singleton(Cat)
provided_cls14 = provider14.cls
assert issubclass(provided_cls14, Cat)
provided_provides14 = provider14.provides
assert provided_provides14 is not None and provided_provides14() == Cat()
assert_type(provided_cls14, Type[Cat])
assert_type(provided_provides14, Callable[..., Cat])

# Test 15: to check class from .provides with explicit typevar
provider15 = providers.Singleton[Animal](Cat)
provided_cls15: Type[Animal] = provider15.cls
assert issubclass(provided_cls15, Animal)
provided_provides15: Optional[Callable[..., Animal]] = provider15.provides
assert provided_provides15 is not None and provided_provides15() == Cat()
assert_type(provided_cls15, Type[Animal])
assert_type(provided_provides15, Callable[..., Animal])

# Test 16: to check string imports
provider16 = providers.Singleton[Any]("builtins.dict")
provider16.set_provides("builtins.dict")
