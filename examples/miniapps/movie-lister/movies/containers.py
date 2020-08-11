"""Containers module."""

from dependency_injector import containers, providers

from . import finders, listers, storages, models, fixtures


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    fixtures = providers.Object(fixtures.MOVIES_SAMPLE_DATA)

    storage = providers.Selector(
        config.storage.type,
        csv=providers.Singleton(
            storages.CsvMovieStorage,
            options=config.storage[config.storage.type],
        ),
        sqlite=providers.Singleton(
            storages.SqliteMovieStorage,
            options=config.storage[config.storage.type],
        ),
    )

    movie = providers.Factory(models.Movie)

    finder = providers.Factory(
        finders.MovieFinder,
        movie_factory=movie.provider,
        movie_storage=storage,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=finder,
    )
