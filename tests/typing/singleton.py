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
provider1 = providers.Singleton(Cat)
animal1: Animal = provider1(1, 2, 3, b='1', c=2, e=0.0)

# Test 2: to check the return type (class factory method)
provider2 = providers.Singleton(Cat.create)
animal2: Animal = provider2()

# Test 3: to check the .override() method
provider3 = providers.Singleton(Animal)
with provider3.override(providers.Singleton(Cat)):
    provider3()

# Test 4: to check the .args, .kwargs, .attributes attributes
provider4 = providers.Singleton(Animal)
args4: Tuple[Any] = provider4.args
kwargs4: Dict[str, Any] = provider4.kwargs
attributes4: Dict[str, Any] = provider4.attributes

# Test 5: to check the provided instance interface
provider5 = providers.Singleton(Animal)
provided5: providers.ProvidedInstance = provider5.provided
attr_getter5: providers.AttributeGetter = provider5.provided.attr
item_getter5: providers.ItemGetter = provider5.provided['item']
method_caller5: providers.MethodCaller = provider5.provided.method.call(123, arg=324)

# Test 6: to check the DelegatedSingleton
provider6 = providers.DelegatedSingleton(Cat)
animal6: Animal = provider6(1, 2, 3, b='1', c=2, e=0.0)

# Test 7: to check the ThreadSafeSingleton
provider7: providers.BaseSingleton[Animal] = providers.ThreadSafeSingleton(Cat)
animal7: Animal = provider7()

# Test 8: to check the DelegatedThreadSafeSingleton
provider8 = providers.DelegatedThreadSafeSingleton(Cat)
animal8: Animal = provider8(1, 2, 3, b='1', c=2, e=0.0)

# Test 9: to check the ThreadLocalSingleton
provider9 = providers.ThreadLocalSingleton(Cat)
animal9: Animal = provider9(1, 2, 3, b='1', c=2, e=0.0)

# Test 10: to check the DelegatedThreadLocalSingleton
provider10 = providers.DelegatedThreadLocalSingleton(Cat)
animal10: Animal = provider10(1, 2, 3, b='1', c=2, e=0.0)

# Test 11: to check the AbstractSingleton
provider11 = providers.AbstractSingleton(Animal)
provider11.override(providers.Singleton(Cat))
animal11: Animal = provider11(1, 2, 3, b='1', c=2, e=0.0)

# Test 12: to check the SingletonDelegate __init__
provider12 = providers.SingletonDelegate(providers.Singleton(object))
