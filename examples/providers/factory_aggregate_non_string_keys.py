"""`FactoryAggregate` provider with non-string keys example."""

from dependency_injector import containers, providers


class Command:
    ...


class CommandA(Command):
    ...


class CommandB(Command):
    ...


class Handler:
    ...


class HandlerA(Handler):
    ...


class HandlerB(Handler):
    ...


class Container(containers.DeclarativeContainer):

    handler_factory = providers.FactoryAggregate({
        CommandA: providers.Factory(HandlerA),
        CommandB: providers.Factory(HandlerB),
    })


if __name__ == "__main__":
    container = Container()

    handler_a = container.handler_factory(CommandA)
    handler_b = container.handler_factory(CommandB)

    assert isinstance(handler_a, HandlerA)
    assert isinstance(handler_b, HandlerB)
