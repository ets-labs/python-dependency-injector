"""A naive example of dependency injection on Python.

Example implementation of dependency injection in Python from Martin Fowler's
article about dependency injection and inversion of control:

http://www.martinfowler.com/articles/injection.html

This mini application uses ``movies`` library, that is configured to work with
sqlite movies database and csv file movies database.
"""

import sqlite3

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import injections

from movies import MoviesModule
from movies import finders

from settings import MOVIES_CSV_PATH
from settings import MOVIES_DB_PATH


class ApplicationModule(catalogs.DeclarativeCatalog):
    """Catalog of application component providers."""

    database = providers.Singleton(sqlite3.connect, MOVIES_DB_PATH)


@catalogs.copy(MoviesModule)
class DbMoviesModule(MoviesModule):
    """Customized catalog of movies module component providers."""

    movie_finder = providers.Factory(finders.SqliteMovieFinder,
                                     *MoviesModule.movie_finder.injections,
                                     database=ApplicationModule.database)


@catalogs.copy(MoviesModule)
class CsvMoviesModule(MoviesModule):
    """Customized catalog of movies module component providers."""

    movie_finder = providers.Factory(finders.CsvMovieFinder,
                                     *MoviesModule.movie_finder.injections,
                                     csv_file=MOVIES_CSV_PATH,
                                     delimeter=',')


@injections.inject(db_movie_lister=DbMoviesModule.movie_lister)
@injections.inject(csv_movie_lister=CsvMoviesModule.movie_lister)
def main(db_movie_lister, csv_movie_lister):
    """Main function.

    This program prints info about all movies that were directed by different
    persons and then prints all movies that were released in 2015.

    :param db_movie_lister: Movie lister, configured to work with database
    :type db_movie_lister: movies.listers.MovieLister

    :param csv_movie_lister: Movie lister, configured to work with csv file
    :type csv_movie_lister: movies.listers.MovieLister
    """
    for movie_lister in (db_movie_lister, csv_movie_lister):
        print movie_lister.movies_directed_by('Francis Lawrence')
        print movie_lister.movies_directed_by('Patricia Riggen')
        print movie_lister.movies_directed_by('JJ Abrams')
        print movie_lister.movies_released_in(2015)


if __name__ == '__main__':
    main()
