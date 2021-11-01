"""Adapters module."""

import abc


class EmailSender(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, to: str, body: str) -> None:
        ...


class SmtpEmailSender:

    def send(self, to: str, body: str) -> None:
        print(f"Sending an email to {to} over SMTP, body=\"{body}\"")


class EchoEmailSender:

    def send(self, to: str, body: str) -> None:
        print(f"Fake sending an email to {to}, body=\"{body}\"")
