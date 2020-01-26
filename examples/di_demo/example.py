"""The Code."""


class Service(object):
    """Some "Service"."""


class Client(object):
    """Some "Client" that uses "Service"."""

    def __init__(self):
        """Initialize instance."""
        self.service = Service()  # Service instance is created inside Client


if __name__ == '__main__':
    client = Client()  # Application creates Client's instance
