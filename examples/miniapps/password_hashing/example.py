"""Example of dependency injection and password hashing in Python."""

import passlib.hash

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class UsersService:
    """Users service."""

    def __init__(self, password_hasher):
        """Initialize instance."""
        self._password_hasher = password_hasher

    def create_user(self, name, password):
        """Create user with hashed password."""
        hashed_password = self._password_hasher(password)
        return dict(name=name, password=hashed_password)


class Container(containers.DeclarativeContainer):
    """Inversion of control container."""

    password_hasher = providers.Callable(
        passlib.hash.sha256_crypt.hash,
        salt_size=16,
        rounds=10000)

    users_service = providers.Factory(
        UsersService,
        password_hasher=password_hasher.provider)


if __name__ == '__main__':
    container = Container()
    users_service = container.users_service()

    user1 = users_service.create_user(name='Roman', password='secret1')
    user2 = users_service.create_user(name='Vitaly', password='secret2')

    print(user1, user2)
