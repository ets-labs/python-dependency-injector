from dependency_injector import providers


# Test 1: to check the return type
provider1 = providers.Delegate(providers.Provider())
var1: providers.Provider = provider1()
