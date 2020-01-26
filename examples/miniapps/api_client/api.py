"""API client module."""


class ApiClient:
    """Some API client."""

    def __init__(self, host, api_key):
        """Initialize instance."""
        self.host = host
        self.api_key = api_key

    def call(self, operation, data):
        """Make some network operations."""
        print('API call [{0}:{1}], method - {2}, data - {3}'.format(
            self.host, self.api_key, operation, repr(data)))
