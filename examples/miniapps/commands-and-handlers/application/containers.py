"""Containers module."""

from dependency_injector import containers, providers

from . import repositories, handler, messagebus, commands


class Container(containers.DeclarativeContainer):

    rating_repository = providers.Singleton(repositories.RatingRepository)

    command_handler = providers.Singleton(
        handler.CommandHandler,
        rating_repo=rating_repository,
    )

    message_bus = providers.Factory(
        messagebus.MessageBus,
        command_handlers=providers.Dict({
            commands.SaveRating: command_handler.provided.save_rating,
            commands.DoSomethingElse: command_handler.provided.something_else,
        }),
    )
