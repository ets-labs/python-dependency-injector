"""Main module."""

import sys

from dependency_injector.wiring import Provide, inject

from .services import UserService, AuthService, PhotoService
from .containers import Container


@inject
def main(
        email: str,
        password: str,
        photo: str,
        user_service: UserService = Provide[Container.user_service],
        auth_service: AuthService = Provide[Container.auth_service],
        photo_service: PhotoService = Provide[Container.photo_service],
) -> None:
    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])
