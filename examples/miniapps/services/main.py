"""Dependency Injector @inject decorator example."""

import application
import dependency_injector.injections as injections


@injections.inject(users_service=application.Services.users)
@injections.inject(auth_service=application.Services.auth)
@injections.inject(photos_service=application.Services.photos)
def main(users_service, auth_service, photos_service):
    """Main function."""
    user = users_service.get_user('user')
    auth_service.authenticate(user, 'secret')
    photos_service.upload_photo(user['id'], 'photo.jpg')


if __name__ == '__main__':
    main()
