from typing import Tuple, Any, Dict

from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):

    def __init__(self, *_, **__): ...

    @classmethod
    def create(cls) -> Animal:
        return cls()


# Test 1: to check the return type (class)
provider1 = providers.Factory(Cat)
animal1: Animal = provider1(1, 2, 3, b='1', c=2, e=0.0)

# Test 2: to check the return type (class factory method)
provider2 = providers.Factory(Cat.create)
animal2: Animal = provider2()

# Test 3: to check the .override() method
provider3 = providers.Factory(Animal)
with provider3.override(providers.Factory(Cat)):
    provider3()

# Test 4: to check the .args, .kwargs, .attributes attributes
provider4 = providers.Factory(Animal)
args4: Tuple[Any] = provider4.args
kwargs4: Dict[str, Any] = provider4.kwargs
attributes4: Dict[str, Any] = provider4.attributes

# Test 5: to check the provided instance interface
provider5 = providers.Factory(Animal)
provided5: providers.ProvidedInstance = provider5.provided
attr_getter5: providers.AttributeGetter = provider5.provided.attr
item_getter5: providers.ItemGetter = provider5.provided['item']
method_caller5: providers.MethodCaller = provider5.provided.method.call(123, arg=324)

# Test 6: to check the DelegatedFactory
provider6 = providers.DelegatedFactory(Cat)
animal6: Animal = provider6(1, 2, 3, b='1', c=2, e=0.0)

# Test 7: to check the AbstractFactory
provider7 = providers.AbstractFactory(Animal)
provider7.override(providers.Factory(Cat))
animal7: Animal = provider7(1, 2, 3, b='1', c=2, e=0.0)

# Test 8: to check the FactoryDelegate __init__
provider8 = providers.FactoryDelegate(providers.Factory(object))

# Test 9: to check FactoryAggregate provider
provider9 = providers.FactoryAggregate(
    a=providers.Factory(object),
    b=providers.Factory(object),
)
factory_a_9: providers.Factory = provider9.a
factory_b_9: providers.Factory = provider9.b
val9: Any = provider9('a')

# Test 10: to check the explicit typing
factory10: providers.Provider[Animal] = providers.Factory(Cat)
animal10: Animal = factory10()

# Test 11: to check the return type with await
provider11 = providers.Factory(Cat)
async def _async11() -> None:
    animal1: Animal = await provider11(1, 2, 3, b='1', c=2, e=0.0)  # type: ignore
    animal2: Animal = await provider11.async_(1, 2, 3, b='1', c=2, e=0.0)
