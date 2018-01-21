"""Dependency injection containers for 'Use Cases' example application."""

from dependency_injector import containers, providers

from example.adapters import SmtpEmailSender, EchoEmailSender
from example.use_cases import SignupUseCase


class Adapters(containers.DeclarativeContainer):
    """Adapters container."""

    email_sender = providers.Singleton(SmtpEmailSender)


class TestAdapters(containers.DeclarativeContainer):
    """Adapters container.

    This container is used for testing purposes.
    """

    email_sender = providers.Singleton(EchoEmailSender)


class UseCases(containers.DeclarativeContainer):
    """Use cases container."""

    adapters = providers.DependenciesContainer()

    signup = providers.Factory(SignupUseCase,
                               email_sender=adapters.email_sender)
