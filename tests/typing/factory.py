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
provider1 = providers.Factory(Cat)
animal1 = provider1(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal1, Cat)

# Test 2: to check the return type (class factory method)
provider2 = providers.Factory(Cat.create)
animal2 = provider2()
assert_type(animal2, Animal)

# Test 3: to check the .override() method
provider3 = providers.Factory(Animal)
with provider3.override(providers.Factory(Cat)):
    animal3 = provider3()
    assert_type(animal3, Animal)

# Test 4: to check the .args, .kwargs, .attributes attributes
provider4 = providers.Factory(Animal)
args4 = provider4.args
kwargs4 = provider4.kwargs
attributes4 = provider4.attributes
assert_type(args4, Tuple[Any])
assert_type(kwargs4, Dict[str, Any])
assert_type(attributes4, Dict[str, Any])

# Test 5: to check the provided instance interface
provider5 = providers.Factory(Animal)
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

# Test 6: to check the DelegatedFactory
provider6 = providers.DelegatedFactory(Cat)
animal6 = provider6(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal6, Cat)

# Test 7: to check the AbstractFactory
provider7 = providers.AbstractFactory(Animal)
provider7.override(providers.Factory(Cat))
animal7 = provider7(1, 2, 3, b="1", c=2, e=0.0)
assert_type(animal7, Animal)

# Test 8: to check the FactoryDelegate __init__
provider8 = providers.FactoryDelegate(providers.Factory(object))

# Test 9: to check FactoryAggregate provider
provider9 = providers.FactoryAggregate(
    a=providers.Factory(str, "str1"),
    b=providers.Factory(str, "str2"),
)
factory_a_9 = provider9.a
factory_b_9 = provider9.b
val9 = provider9("a")
assert_type(provider9, providers.FactoryAggregate[str])
assert_type(factory_a_9, providers.Factory[str])
assert_type(factory_b_9, providers.Factory[str])
assert_type(val9, str)

provider9_set_non_string_keys = providers.FactoryAggregate[str]()
provider9_set_non_string_keys.set_factories({Cat: providers.Factory(str, "str")})
factory_set_non_string_9 = provider9_set_non_string_keys.factories[Cat]
assert_type(provider9_set_non_string_keys, providers.FactoryAggregate[str])
assert_type(factory_set_non_string_9, providers.Factory[str])

provider9_new_non_string_keys = providers.FactoryAggregate(
    {Cat: providers.Factory(str, "str")},
)
factory_new_non_string_9 = provider9_new_non_string_keys.factories[Cat]
assert_type(provider9_new_non_string_keys, providers.FactoryAggregate[str])
assert_type(factory_new_non_string_9, providers.Factory[str])

provider9_no_explicit_typing = providers.FactoryAggregate(
    a=providers.Factory(str, "str")
)
provider9_no_explicit_typing_factory = provider9_no_explicit_typing.factories["a"]
provider9_no_explicit_typing_object = provider9_no_explicit_typing("a")
assert_type(provider9_no_explicit_typing, providers.FactoryAggregate[str])
assert_type(provider9_no_explicit_typing_factory, providers.Factory[str])
assert_type(provider9_no_explicit_typing_object, str)

# Test 10: to check the explicit typing
factory10 = providers.Factory[Animal](Cat)
animal10 = factory10()
assert_type(factory10, providers.Factory[Animal])
assert_type(animal10, Animal)

# Test 11: to check the return type with await
provider11 = providers.Factory(Cat)


async def _async11() -> None:
    animal1 = await provider11(1, 2, 3, b="1", c=2, e=0.0)  # type: ignore
    animal2 = await provider11.async_(1, 2, 3, b="1", c=2, e=0.0)
    assert_type(animal2, Cat)


# Test 12: to check class type from .provides
provider12 = providers.Factory(Cat)
provided_cls12 = provider12.cls
assert issubclass(provided_cls12, Animal)
provided_provides12 = provider12.provides
assert provided_provides12 is not None and provided_provides12() == Cat()
assert_type(provided_cls12, Type[Cat])
assert_type(provided_provides12, Callable[..., Cat])


# Test 13: to check class from .provides with explicit typevar
provider13 = providers.Factory[Animal](Cat)
provided_cls13 = provider13.cls
assert issubclass(provided_cls13, Animal)
provided_provides13 = provider13.provides
assert provided_provides13 is not None and provided_provides13() == Cat()
assert_type(provided_cls13, Type[Animal])
assert_type(provided_provides13, Callable[..., Animal])

# Test 14: to check string imports
provider14 = providers.Factory[Any]("builtins.dict")
provider14.set_provides("builtins.dict")
