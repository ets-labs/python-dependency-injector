"""Main module."""

from .containers import Container
from .commands import SaveRating, DoSomethingElse


if __name__ == "__main__":
    container = Container()
    message_bus = container.message_bus()

    message_bus.handle(SaveRating)
    message_bus.handle(DoSomethingElse)
