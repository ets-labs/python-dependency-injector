from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):

    @classmethod
    def create(cls) -> Animal:
        return cls()


# Test 1: to check the return type (class)
provider1 = providers.Factory(Cat)
animal1: Animal = provider1(1, 2, 3, b='1', c=2, e=0.0)

# Test 2: to check the return type (class factory method)
provider2 = providers.Factory(Cat.create)
animal2: Animal = provider2()
