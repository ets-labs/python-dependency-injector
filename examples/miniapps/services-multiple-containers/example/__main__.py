"""Main module."""

import sys

from .containers import Application


def main(email: str, password: str, photo: str) -> None:
    application = Application()

    application.config.from_yaml('config.yml')
    application.core.configure_logging()

    user_service = application.services.user()
    auth_service = application.services.auth()
    photo_service = application.services.photo()

    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)


if __name__ == '__main__':
    main(*sys.argv[1:])
