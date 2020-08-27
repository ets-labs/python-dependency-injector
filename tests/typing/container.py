from dependency_injector import providers


class Container:
    ...


# Test 1: to check the return type
provider1 = providers.Container(Container)
var1: Container = provider1()

# Test 2: to check the getattr
provider2 = providers.Container(Container)
attr: providers.Provider = provider2.attr
