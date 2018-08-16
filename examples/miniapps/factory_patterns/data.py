"""Sample data classes."""


class SqlAlchemyDatabaseService:
    """Database service of an entity."""

    def __init__(self, session, base_class):
        """Initialize object."""
        self.session = session
        self.base_class = base_class


class TokensService:
    """Tokens service."""

    def __init__(self, id_generator, database):
        """Initialize object."""
        self.id_generator = id_generator
        self.database = database


class Token:
    """Token entity."""


class UsersService:
    """Users service."""

    def __init__(self, id_generator, database):
        """Initialize object."""
        self.id_generator = id_generator
        self.database = database


class User:
    """User entity."""


# Sample objects
session = object()
id_generator = object()
