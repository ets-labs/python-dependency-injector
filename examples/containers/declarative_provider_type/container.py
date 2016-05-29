"""Specialized declarative IoC container example."""

import core
import services


class Services(core.ServicesContainer):
    """IoC container of service providers."""

    users = core.ServiceProvider(services.UsersService,
                                 config={'option1': '111',
                                         'option2': '222'})

    auth = core.ServiceProvider(services.AuthService,
                                config={'option3': '333',
                                        'option4': '444'},
                                users_service=users)
