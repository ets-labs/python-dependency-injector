"""Example main module."""


def main(uid, password, photo, users_service, auth_service, photos_service):
    """Authenticate user and upload photo."""
    user = users_service.get_user_by_id(uid)
    auth_service.authenticate(user, password)
    photos_service.upload_photo(user['uid'], photo)
