"""`Singleton` provider resetting example."""

from dependency_injector import providers


class UserService:
    ...


user_service_provider = providers.Singleton(UserService)


if __name__ == '__main__':
    user_service1 = user_service_provider()

    user_service_provider.reset()

    users_service2 = user_service_provider()
    assert users_service2 is not user_service1
