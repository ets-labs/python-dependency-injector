"""A naive example of dependency injection in Python.

Example implementation of dependency injection in Python from Martin Fowler's
article about dependency injection and inversion of control.

http://www.martinfowler.com/articles/injection.html
"""

import sqlite3

from movies.module import MoviesModule
from movies.components import SqliteMovieFinder

from settings import MOVIES_DB_PATH

from dependency_injector import catalogs
from dependency_injector import providers


class ApplicationModule(catalogs.DeclarativeCatalog):
    """Catalog of application components."""

    database = providers.Singleton(sqlite3.connect,
                                   MOVIES_DB_PATH)
    """:type: providers.Provider -> components.MovieFinder"""


@catalogs.override(MoviesModule)
class MyMoviesModule(catalogs.DeclarativeCatalog):
    """Customized catalog of movie module components."""

    movie_finder = providers.Factory(SqliteMovieFinder,
                                     database=ApplicationModule.database)


def main():
    """Main function."""
    movie_lister = MoviesModule.movie_lister()

    print movie_lister.movies_directed_by('Francis Lawrence')
    print movie_lister.movies_directed_by('Patricia Riggen')
    print movie_lister.movies_directed_by('JJ Abrams')

    print movie_lister.movies_released_in(2015)


if __name__ == '__main__':
    main()
