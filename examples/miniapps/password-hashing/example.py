"""Password hashing example."""

from typing import Callable, Dict

import passlib.hash

from dependency_injector import containers, providers


class UserService:

    def __init__(self, password_hasher: Callable[[str], str]) -> None:
        self._password_hasher = password_hasher

    def create_user(self, name: str, password: str) -> Dict[str, str]:
        hashed_password = self._password_hasher(password)
        return {
            "name": name,
            "password": hashed_password,
        }


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    password_hasher = providers.Callable(
        passlib.hash.sha256_crypt.hash,
        salt_size=config.salt_size,
        rounds=config.rounds,
    )

    user_service = providers.Factory(
        UserService,
        password_hasher=password_hasher.provider,
    )


if __name__ == "__main__":
    container = Container(
        config={
            "salt_size": 16,
            "rounds": 10000,
        },
    )

    user_service = container.user_service()

    user = user_service.create_user(name="Roman", password="secret1")
    print(user)
