"""Example main module."""


def main(uid, password, photo, users_service, auth_service, photos_service):
    """Authenticate user and upload photo.

    :param uid: User identifier.
    :type uid: int

    :param password: User's password for verification.
    :type password: str

    :param photo_path: Path to photo for uploading.
    :type photo_path: str

    :param users_service: Users service.
    :type users_service: example.services.UsersService

    :param auth_service: Authentication service.
    :type auth_service: example.services.AuthService

    :param photo_service: Photo service.
    :type photo_service: example.services.PhotoService
    """
    user = users_service.get_user_by_id(uid)
    auth_service.authenticate(user, password)
    photos_service.upload_photo(user['uid'], photo)
