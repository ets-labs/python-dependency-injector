"""Example use cases package."""


class UseCase:
    """Abstract use case."""

    def execute(self):
        """Execute use case handling."""
        raise NotImplementedError()


class SignupUseCase:
    """Sign up use cases registers users."""

    def __init__(self, email_sender):
        """Initialize instance."""
        self.email_sender = email_sender

    def execute(self, email):
        """Execute use case handling."""
        print('Sign up user {0}'.format(email))
        self.email_sender.send(email, 'Welcome, "{}"'.format(email))
