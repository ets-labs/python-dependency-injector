"""The Code, that demonstrates dependency injection pattern."""


class Service:
    """Some "Service"."""


class Client:
    """Some "Client" that uses "Service"."""

    def __init__(self, service):  # Service instance is injected into Client
        """Initialize instance."""
        self.service = service


if __name__ == '__main__':
    service = Service()       # Application creates Service instance
    client = Client(service)  # and inject Service instance into the Client
