"""The Code, that follows Inversion of Control principle."""


class Service(object):
    """Some "Service"."""


class Client(object):
    """Some "Client" that uses "Service"."""

    def __init__(self, service):  # Service instance is injected in Client
        """Initializer."""
        self.service = service


if __name__ == '__main__':
    # Application creates Service instance
    service = Service()

    # and inject Service instance into the Client
    client = Client(service)
