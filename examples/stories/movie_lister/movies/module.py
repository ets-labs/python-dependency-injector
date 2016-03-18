"""Movies package dependency injection module."""

from . import components

from dependency_injector import catalogs
from dependency_injector import providers


class MoviesModule(catalogs.DeclarativeCatalog):
    """Catalog of movie module components."""

    movie_finder = providers.Factory(components.MovieFinder)
    """:type: providers.Provider -> components.MovieFinder"""

    movie_lister = providers.Factory(components.MovieLister,
                                     movie_finder=movie_finder)
    """:type: providers.Provider -> components.MovieLister"""
