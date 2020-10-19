from dependency_injector import providers


# Test 1: to check .provided attribute
provider1: providers.Provider[int] = providers.Object(1)
provided: providers.ProvidedInstance = provider1.provided
