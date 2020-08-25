from typing import Type

from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):

    def __init__(self, *_, **__): ...


# Test 1: to check the return type
provider1 = providers.Dependency(instance_of=Animal)
provider1.override(providers.Factory(Cat))
var1: Animal = provider1()

# Test 2: to check the return type
provider2 = providers.Dependency(instance_of=Animal)
var2: Type[Animal] = provider2.instance_of
