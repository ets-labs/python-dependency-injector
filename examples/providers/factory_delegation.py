"""`Factory` provider delegation example."""

from typing import Callable, List

from dependency_injector import containers, providers


class User:
    def __init__(self, uid: int) -> None:
        self.uid = uid


class UserRepository:
    def __init__(self, user_factory: Callable[..., User]) -> None:
        self.user_factory = user_factory

    def get_all(self) -> List[User]:
        return [
            self.user_factory(**user_data)
            for user_data in [{"uid": 1}, {"uid": 2}]
        ]


class Container(containers.DeclarativeContainer):

    user_factory = providers.Factory(User)

    user_repository_factory = providers.Factory(
        UserRepository,
        user_factory=user_factory.provider,
    )


if __name__ == "__main__":
    container = Container()

    user_repository = container.user_repository_factory()

    user1, user2 = user_repository.get_all()

    assert user1.uid == 1
    assert user2.uid == 2
