"""Message bus module."""

from typing import Dict, Callable, Any

from .commands import Command


class MessageBus:

    def __init__(self, command_handlers: Dict[str, Callable[..., Any]]):
        self.command_handlers = command_handlers

    def handle(self, command: Command):
        self.command_handlers[command]()
