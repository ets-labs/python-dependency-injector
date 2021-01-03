from typing import Tuple, Any, Dict

from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):

    @classmethod
    def create(cls) -> Animal:
        return cls()


# Test 1: to check the return type (class)
provider1 = providers.Callable(Cat)
animal1: Animal = provider1(1, 2, 3, b='1', c=2, e=0.0)

# Test 2: to check the return type (class factory method)
provider2 = providers.Callable(Cat.create)
animal2: Animal = provider2()

# Test 3: to check the .override() method
provider3 = providers.Callable(Animal)
with provider3.override(providers.Callable(Cat)):
    provider3()

# Test 4: to check the .args & .kwargs attributes
provider4 = providers.Callable(Animal)
args4: Tuple[Any] = provider4.args
kwargs4: Dict[str, Any] = provider4.kwargs

# Test 5: to check the provided instance interface
provider5 = providers.Callable(Animal)
provided5: providers.ProvidedInstance = provider5.provided
attr_getter5: providers.AttributeGetter = provider5.provided.attr
item_getter5: providers.ItemGetter = provider5.provided['item']
method_caller: providers.MethodCaller = provider5.provided.method.call(123, arg=324)

# Test 6: to check the DelegatedCallable
provider6 = providers.DelegatedCallable(Cat)
animal6: Animal = provider6(1, 2, 3, b='1', c=2, e=0.0)

# Test 7: to check the AbstractCallable
provider7 = providers.AbstractCallable(Animal)
provider7.override(providers.Callable(Cat))
animal7: Animal = provider7(1, 2, 3, b='1', c=2, e=0.0)

# Test 8: to check the CallableDelegate __init__
provider8 = providers.CallableDelegate(providers.Callable(lambda: None))

# Test 9: to check the return type with await
provider9 = providers.Callable(Cat)
async def _async9() -> None:
    animal1: Animal = await provider9(1, 2, 3, b='1', c=2, e=0.0)  # type: ignore
    animal2: Animal = await provider9.async_(1, 2, 3, b='1', c=2, e=0.0)
