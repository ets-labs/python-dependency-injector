"""Example main module."""


def main(users_service, auth_service, photos_service):
    """Example main function."""
    user = users_service.get_user('user')
    auth_service.authenticate(user, 'secret')
    photos_service.upload_photo(user['id'], 'photo.jpg')
