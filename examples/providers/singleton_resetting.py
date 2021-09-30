"""`Singleton` provider resetting example."""

from dependency_injector import containers, providers


class UserService:
    ...


class Container(containers.DeclarativeContainer):

    user_service = providers.Singleton(UserService)


if __name__ == "__main__":
    container = Container()

    user_service1 = container.user_service()

    container.user_service.reset()

    user_service2 = container.user_service()
    assert user_service2 is not user_service1
