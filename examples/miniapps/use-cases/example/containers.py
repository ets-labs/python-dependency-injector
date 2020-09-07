"""Containers module."""

from dependency_injector import containers, providers

from . import adapters, usecases


class Adapters(containers.DeclarativeContainer):

    email_sender = providers.Singleton(adapters.SmtpEmailSender)


class TestAdapters(containers.DeclarativeContainer):

    email_sender = providers.Singleton(adapters.EchoEmailSender)


class UseCases(containers.DeclarativeContainer):

    adapters = providers.DependenciesContainer()

    signup = providers.Factory(
        usecases.SignupUseCase,
        email_sender=adapters.email_sender,
    )
