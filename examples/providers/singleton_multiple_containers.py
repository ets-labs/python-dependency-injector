"""`Singleton` provider resetting example."""

from dependency_injector import containers, providers


class UserService:
    ...


class Container(containers.DeclarativeContainer):

    user_service_provider = providers.Singleton(UserService)


if __name__ == "__main__":
    container1 = Container()
    user_service1 = container1.user_service_provider()
    assert user_service1 is container1.user_service_provider()

    container2 = Container()
    user_service2 = container2.user_service_provider()
    assert user_service2 is container2.user_service_provider()

    assert user_service1 is not user_service2
