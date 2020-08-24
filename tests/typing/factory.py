from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):
    ...


provider = providers.Factory(Cat)

animal: Animal = provider(1, 2, 3, b='1', c=2, e=0.0)
