"""Base classes for services."""

import core


class UsersService(core.BaseService):
    """Users service."""

    def __init__(self, config):
        """Initializer."""
        self.config = config
        super(UsersService, self).__init__()


class AuthService(core.BaseService):
    """Auth service."""

    def __init__(self, config, users_service):
        """Initializer."""
        self.config = config
        self.users_service = users_service
        super(AuthService, self).__init__()
