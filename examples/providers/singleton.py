"""`Singleton` provider example."""

from dependency_injector import containers, providers


class UserService:
    ...


class Container(containers.DeclarativeContainer):

    user_service_provider = providers.Singleton(UserService)


if __name__ == "__main__":
    container = Container()

    user_service1 = container.user_service_provider()
    user_service2 = container.user_service_provider()
    assert user_service1 is user_service2
