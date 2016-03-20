"""Movies package."""

from . import finders
from . import listers
from . import models

from dependency_injector import catalogs
from dependency_injector import providers


class MoviesModule(catalogs.DeclarativeCatalog):
    """Catalog of movies module components."""

    movie_model = providers.DelegatedFactory(models.Movie)
    """:type: providers.Provider -> models.Movie"""

    movie_finder = providers.Factory(finders.MovieFinder,
                                     movie_model=movie_model)
    """:type: providers.Provider -> finders.MovieFinder"""

    movie_lister = providers.Factory(listers.MovieLister,
                                     movie_finder=movie_finder)
    """:type: providers.Provider -> listers.MovieLister"""
