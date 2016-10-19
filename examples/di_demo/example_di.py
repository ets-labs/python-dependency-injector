"""The Code, that demonstrates dependency injection pattern."""


class Service(object):
    """Some "Service"."""


class Client(object):
    """Some "Client" that uses "Service"."""

    def __init__(self, service):  # Service instance is injected into Client
        """Initializer."""
        self.service = service


if __name__ == '__main__':
    service = Service()       # Application creates Service instance
    client = Client(service)  # and inject Service instance into the Client
