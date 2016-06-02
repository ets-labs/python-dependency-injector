"""Movies package.

Top-level package of movies library. This package contains IoC container of
movies module component providers - ``MoviesModule``. It is recommended to use
movies library functionality by fetching required instances from
``MoviesModule`` providers.

``MoviesModule.movie_finder`` is a factory that provides abstract component
``finders.MovieFinder``. This provider should be overridden by provider of
concrete finder implementation in terms of library configuration.

Each of ``MoviesModule`` providers could be overridden.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

import movies.finders
import movies.listers
import movies.models


class MoviesModule(containers.DeclarativeContainer):
    """IoC container of movies module component providers."""

    movie_model = providers.DelegatedFactory(movies.models.Movie)

    movie_finder = providers.Factory(movies.finders.MovieFinder,
                                     movie_model=movie_model)

    movie_lister = providers.Factory(movies.listers.MovieLister,
                                     movie_finder=movie_finder)
