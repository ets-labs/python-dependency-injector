from dependency_injector import containers, providers


# Test 1: to check declarative container subclass
class Container1(containers.DeclarativeContainer):
    provider = providers.Factory(int)


container1 = Container1()
container1_type: containers.Container = Container1()
provider1: providers.Provider = container1.provider
val1: int = container1.provider(3)
