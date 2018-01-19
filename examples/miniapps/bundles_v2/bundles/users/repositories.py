"""Users bundle entity repositories module."""


class UserRepository(object):
    """User entity repository."""

    def __init__(self, object_factory, db):
        """Initializer."""
        self.object_factory = object_factory
        self.db = db

    def get(self, id):
        """Return user entity with given identifier."""
        return self.object_factory(id=id)
