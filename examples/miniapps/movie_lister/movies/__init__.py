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

from dependency_injector import containers
from dependency_injector import providers

from . import finders
from . import listers
from . import models


class MoviesModule(containers.DeclarativeContainer):
    """IoC container of movies module component providers."""

    movie_model = providers.DelegatedFactory(models.Movie)

    movie_finder = providers.Factory(finders.MovieFinder,
                                     movie_model=movie_model)

    movie_lister = providers.Factory(listers.MovieLister,
                                     movie_finder=movie_finder)
