"""The Code."""


class Service:
    """The Service."""


class Client:
    """The Client that uses the Service."""

    def __init__(self):
        """Initialize the Client."""
        self.service = Service()  # The Service is created by the Client


if __name__ == '__main__':
    client = Client()  # Application creates the Client
