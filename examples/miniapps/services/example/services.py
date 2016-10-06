"""Example business services module."""


class Users(object):
    """Users service."""

    def __init__(self, logger, db):
        """Initializer."""
        self.logger = logger
        self.db = db

    def get_user_by_id(self, uid):
        """Return user's information by login."""
        self.logger.debug('User %s has been found in database', uid)
        return {'uid': uid,
                'password_hash': 'secret_hash'}


class Auth(object):
    """Auth service."""

    def __init__(self, logger, db, token_ttl):
        """Initializer."""
        self.logger = logger
        self.db = db
        self.token_ttl = token_ttl

    def authenticate(self, user, password):
        """Authenticate user."""
        assert user['password_hash'] == '_'.join((password, 'hash'))
        self.logger.debug('User %s has been successfully authenticated',
                          user['uid'])


class Photos(object):
    """Photos service."""

    def __init__(self, logger, db, s3):
        """Initializer."""
        self.logger = logger
        self.db = db
        self.s3 = s3

    def upload_photo(self, uid, photo_path):
        """Upload user photo."""
        self.logger.debug('Photo %s has been successfully uploaded by user %s',
                          photo_path, uid)
