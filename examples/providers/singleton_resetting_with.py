"""`Singleton` provider resetting context manager example."""

from dependency_injector import containers, providers


class UserService:
    ...


class Container(containers.DeclarativeContainer):

    user_service = providers.Singleton(UserService)


if __name__ == "__main__":
    container = Container()

    user_service1 = container.user_service()

    with container.user_service.reset():
        user_service2 = container.user_service()

    user_service3 = container.user_service()

    assert user_service1 is not user_service2
    assert user_service2 is not user_service3
    assert user_service3 is not user_service1
