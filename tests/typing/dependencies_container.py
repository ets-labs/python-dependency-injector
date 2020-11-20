from dependency_injector import providers


# Test 1: to check the getattr type
provider1 = providers.DependenciesContainer(
    a=providers.Provider(),
    b=providers.Provider(),
)
a1: providers.Provider = provider1.a
b1: providers.Provider = provider1.b
c1: providers.ProvidedInstance = provider1.c.provided
