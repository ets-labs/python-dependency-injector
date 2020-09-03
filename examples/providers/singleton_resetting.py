"""`Singleton` provider resetting example."""

from dependency_injector import containers, providers


class UserService:
    ...


class Container(containers.DeclarativeContainer):

    user_service_provider = providers.Singleton(UserService)


if __name__ == '__main__':
    container = Container()

    user_service1 = container.user_service_provider()

    container.user_service_provider.reset()

    user_service2 = container.user_service_provider()
    assert user_service2 is not user_service1
