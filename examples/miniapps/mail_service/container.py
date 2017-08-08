"""Mail service and user registration DI container example."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Singleton

import example


class Container(DeclarativeContainer):
    """DI container."""

    mail_service = Singleton(example.MailService,
                             host='localhost',
                             port=587,
                             login='my_login',
                             password='super_secret_password')

    add_user = Callable(example.add_user,
                        mailer=mail_service)


if __name__ == '__main__':
    print('Using real mail service:')
    Container.add_user('sample@mail.com', 'password')
    # Using real mail service:
    # Connecting server localhost:587 with my_login:super_secret_password
    # Sending "Your password is password" to "sample@mail.com"

    print('Using mail service stub:')
    Container.add_user('sample@mail.com', 'password',
                       mailer=example.MailServiceStub())
    # Using mail service stub:
    # Emulating sending "Your password is password" to "sample@mail.com"

    # Also you can override provider by another provider:
    Container.mail_service.override(Singleton(example.MailServiceStub))
    print('Using mail service stub by overriding mail service provider:')
    Container.add_user('sample@mail.com', 'password')
    # Using mail service stub by overriding mail service provider:
    # Emulating sending "Your password is password" to "sample@mail.com"
    Container.mail_service.reset_override()  # Resetting provider overriding
