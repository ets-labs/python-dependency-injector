"""Dependency Injector @inject decorator example."""

import dependency_injector.injections as di
import containers


@di.inject(users_service=containers.Services.users)
@di.inject(auth_service=containers.Services.auth)
@di.inject(photos_service=containers.Services.photos)
def main(users_service, auth_service, photos_service):
    """Main function."""
    user = users_service.get_user('user')
    auth_service.authenticate(user, 'secret')
    photos_service.upload_photo(user['id'], 'photo.jpg')


if __name__ == '__main__':
    main()
