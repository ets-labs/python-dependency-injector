"""Photos bundle entity repositories module."""


class PhotoRepository(object):
    """Photo entity repository."""

    def __init__(self, object_factory, fs, db):
        """Initialize instance."""
        self.object_factory = object_factory
        self.fs = fs
        self.db = db
