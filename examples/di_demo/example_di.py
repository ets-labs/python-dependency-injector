"""The Code that demonstrates dependency injection pattern."""


class Service:
    """The Service."""


class Client:
    """The Client that uses the Service."""

    def __init__(self, service):  # The Service is injected into the Client
        """Initialize the Client."""
        self.service = service


if __name__ == '__main__':
    service = Service()       # Application creates the Service
    client = Client(service)  # and inject the Service into the Client
