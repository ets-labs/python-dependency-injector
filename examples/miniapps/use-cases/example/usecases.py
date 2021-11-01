"""Use cases module."""

import abc

from .adapters import EmailSender


class UseCase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self) -> None:
        ...


class SignupUseCase:

    def __init__(self, email_sender: EmailSender) -> None:
        self.email_sender = email_sender

    def execute(self, email: str) -> None:
        print(f"Sign up user {email}")
        self.email_sender.send(email, f"Welcome, {email}")
