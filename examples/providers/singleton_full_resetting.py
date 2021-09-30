"""`Singleton` provider full resetting example."""

from dependency_injector import containers, providers


class Database:
    ...


class UserService:
    def __init__(self, db: Database):
        self.db = db


class Container(containers.DeclarativeContainer):

    database = providers.Singleton(Database)

    user_service = providers.Singleton(UserService, db=database)


if __name__ == "__main__":
    container = Container()

    user_service1 = container.user_service()

    container.user_service.full_reset()

    user_service2 = container.user_service()
    assert user_service2 is not user_service1
    assert user_service2.db is not user_service1.db
