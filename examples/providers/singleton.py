"""`Singleton` provider example."""

from dependency_injector import providers


class UserService:
    ...


user_service_provider = providers.Singleton(UserService)


if __name__ == '__main__':
    user_service1 = user_service_provider()
    user_service2 = user_service_provider()
    assert user_service1 is user_service2
