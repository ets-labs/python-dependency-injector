from dependency_injector import containers, providers


# Test 1: to check declarative container subclass
class Container1(containers.DeclarativeContainer):
    provider = providers.Factory(int)


container1 = Container1()
container1_type: containers.Container = Container1()
provider1: providers.Provider = container1.provider
val1: int = container1.provider(3)


# Test 2: to check @override decorator
class Container21(containers.DeclarativeContainer):
    provider = providers.Factory(int)


@containers.override(Container21)
class Container22(containers.DeclarativeContainer):
    ...


# Test 3: to check @copy decorator
class Container31(containers.DeclarativeContainer):
    provider = providers.Factory(int)


@containers.copy(Container31)
class Container32(containers.DeclarativeContainer):
    ...


# Test 4: to override()
class Container4(containers.DeclarativeContainer):
    provider = providers.Factory(int)

container4 = Container4()
container4.override(Container4())
