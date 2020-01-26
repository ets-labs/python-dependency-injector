"""Mail service and user registration example."""


class AbstractMailService(object):
    """Abstract mail service."""

    def send(self, email, body):
        """Send email."""
        raise NotImplementedError()


class MailService(AbstractMailService):
    """Mail service."""

    def __init__(self, host, port, login, password):
        """Initialize instance."""
        self._host = host
        self._port = port
        self._login = login
        self._password = password

    def send(self, email, body):
        """Send email."""
        print('Connecting server {0}:{1} with {2}:{3}'.format(
            self._host, self._port, self._login, self._password))
        print('Sending "{0}" to "{1}"'.format(body, email))


class MailServiceStub(AbstractMailService):
    """Mail service stub."""

    def send(self, email, body):
        """Send email."""
        print('Emulating sending "{0}" to "{1}"'.format(body, email))


def add_user(email, password, mailer):
    """Register user."""
    mailer.send(email, 'Your password is {0}'.format(password))
