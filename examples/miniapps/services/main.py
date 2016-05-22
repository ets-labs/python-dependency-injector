"""Dependency Injector @inject decorator example."""

from dependency_injector.injections import inject

from catalogs import Services


@inject(users_service=Services.users)
@inject(auth_service=Services.auth)
@inject(photos_service=Services.photos)
def main(users_service, auth_service, photos_service):
    """Main function."""
    user = users_service.get_user('user')
    auth_service.authenticate(user, 'secret')
    photos_service.upload_photo(user['id'], 'photo.jpg')


if __name__ == '__main__':
    main()
