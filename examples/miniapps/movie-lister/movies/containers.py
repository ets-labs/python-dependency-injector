"""Containers module."""

from dependency_injector import containers, providers

from . import finders, listers, entities


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    movie = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.sqlite.path,
    )

    finder = providers.Selector(
        config.finder.type,
        csv=csv_finder,
        sqlite=sqlite_finder,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=finder,
    )
