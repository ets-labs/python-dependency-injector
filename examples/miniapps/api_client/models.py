"""Models module."""


class User:
    """User model."""

    def __init__(self, id, api_client):
        """Initialize instance."""
        self.id = id
        self.api_client = api_client

    def register(self):
        """Register user."""
        self.api_client.call('register', {'id': self.id})
