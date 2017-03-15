"""Example business services module."""


class BaseService(object):
    """Service base class."""


class UsersService(BaseService):
    """Users service."""

    def __init__(self, logger, db):
        """Initializer.

        :param logger: Logger instance.
        :type logger: logging.Logger

        :param db: Database connection.
        :type db: sqlite3.Connection
        """
        self.logger = logger
        self.db = db

    def get_user_by_id(self, uid):
        """Return user's data by identifier.

        :param uid: User identifier.
        :type uid: int

        :rtype: dict
        """
        self.logger.debug('User %s has been found in database', uid)
        return dict(uid=uid, password_hash='secret_hash')


class AuthService(BaseService):
    """Authentication service."""

    def __init__(self, logger, db, token_ttl):
        """Initializer.

        :param logger: Logger instance.
        :type logger: logging.Logger

        :param db: Database connection.
        :type db: sqlite3.Connection

        :param token_ttl: Token lifetime in seconds.
        :type token_ttl: int
        """
        self.logger = logger
        self.db = db
        self.token_ttl = token_ttl

    def authenticate(self, user, password):
        """Authenticate user.

        :param user: User's data.
        :type user: dict

        :param password: User's password for verification.
        :type password: str

        :raises: AssertionError when password is wrong

        :rtype: None
        """
        assert user['password_hash'] == '_'.join((password, 'hash'))
        self.logger.debug('User %s has been successfully authenticated',
                          user['uid'])


class PhotosService(BaseService):
    """Photos service."""

    def __init__(self, logger, db, s3):
        """Initializer.

        :param logger: Logger instance.
        :type logger: logging.Logger

        :param db: Database connection.
        :type db: sqlite3.Connection

        :param s3: AWS S3 client.
        :type s3: botocore.client.S3
        """
        self.logger = logger
        self.db = db
        self.s3 = s3

    def upload_photo(self, uid, photo_path):
        """Upload user photo.

        :param uid: User identifier.
        :type uid: int

        :param photo_path: Path to photo for uploading.
        :type photo_path: str

        :rtpe: None
        """
        self.logger.debug('Photo %s has been successfully uploaded by user %s',
                          photo_path, uid)
