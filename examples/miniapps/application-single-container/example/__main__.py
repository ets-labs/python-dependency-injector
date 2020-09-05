"""Main module."""

import sys

from .containers import Container


def main(email: str, password: str, photo: str) -> None:
    container = Container()

    container.configure_logging()
    container.config.from_ini('config.ini')

    user_service = container.user_service()
    auth_service = container.auth_service()
    photo_service = container.photo_service()

    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)


if __name__ == '__main__':
    main(*sys.argv[1:])
