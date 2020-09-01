"""`Factory` providers example."""

from dependency_injector import providers


class User:
    ...


users_factory = providers.Factory(User)


if __name__ == '__main__':
    user1 = users_factory()
    user2 = users_factory()
