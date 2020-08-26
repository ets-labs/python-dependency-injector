from dependency_injector import providers


# Test 1: to check the return type
provider1 = providers.Selector(
    lambda: 'a',
    a=providers.Factory(object),
    b=providers.Factory(object),
)
var1: int = provider1()

# Test 2: to check the provided instance interface
provider2 = providers.Selector(
    lambda: 'a',
    a=providers.Factory(object),
    b=providers.Factory(object),
)
provided2: providers.ProvidedInstance = provider2.provided
attr_getter2: providers.AttributeGetter = provider2.provided.attr
item_getter2: providers.ItemGetter = provider2.provided['item']
method_caller2: providers.MethodCaller = provider2.provided.method.call(123, arg=324)

# Test3 to check the getattr
provider3 = providers.Selector(
    lambda: 'a',
    a=providers.Factory(object),
    b=providers.Factory(object),
)
attr3: providers.Provider = provider3.a
