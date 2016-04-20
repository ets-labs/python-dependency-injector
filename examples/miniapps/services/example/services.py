"""Example business services module."""


class Users(object):
    """Users service."""

    def __init__(self, db):
        """Initializer."""
        self.db = db

    def get_user(self, login):
        """Return user's information by login."""
        return {'id': 1,
                'login': login,
                'password_hash': 'secret_hash'}


class Auth(object):
    """Auth service."""

    def __init__(self, db, token_ttl):
        """Initializer."""
        self.db = db
        self.token_ttl = token_ttl

    def authenticate(self, user, password):
        """Authenticate user."""
        assert user['password_hash'] == '_'.join((password, 'hash'))


class Photos(object):
    """Photos service."""

    def __init__(self, db, s3):
        """Initializer."""
        self.db = db
        self.s3 = s3

    def upload_photo(self, user_id, photo_path):
        """Upload user photo."""
