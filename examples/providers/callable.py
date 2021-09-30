"""`Callable` provider example."""

import passlib.hash

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    password_hasher = providers.Callable(
        passlib.hash.sha256_crypt.hash,
        salt_size=16,
        rounds=10000,
    )

    password_verifier = providers.Callable(passlib.hash.sha256_crypt.verify)


if __name__ == "__main__":
    container = Container()

    hashed_password = container.password_hasher("super secret")
    assert container.password_verifier("super secret", hashed_password)
