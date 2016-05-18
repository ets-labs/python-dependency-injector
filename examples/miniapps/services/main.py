"""Dependency Injector example."""

from dependency_injector.injections import inject

from catalogs import Services


@inject(users_service=Services.users)
@inject(auth_service=Services.auth)
@inject(photos_service=Services.photos)
def main(login, password, photo, users_service, auth_service, photos_service):
    """Main function."""
    user = users_service.get_user(login)
    auth_service.authenticate(user, password)
    photos_service.upload_photo(user['id'], photo)


if __name__ == '__main__':
    main(login='user', password='secret', photo='photo.jpg')
