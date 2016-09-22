"""A naive example of dependency injection on Python.

Example implementation of dependency injection in Python from Martin Fowler's
article about dependency injection and inversion of control:

http://www.martinfowler.com/articles/injection.html

This mini application uses ``movies`` library, that is configured to work with
csv file movies database.
"""

import movies
import movies.finders

import example.db
import example.main

import settings

import dependency_injector.containers as containers
import dependency_injector.providers as providers


@containers.override(movies.MoviesModule)
class MyMoviesModule(containers.DeclarativeContainer):
    """IoC container for overriding movies module component providers."""

    movie_finder = providers.Factory(movies.finders.CsvMovieFinder,
                                     csv_file_path=settings.MOVIES_CSV_PATH,
                                     delimiter=',',
                                     **movies.MoviesModule.movie_finder.kwargs)


class CsvApplication(containers.DeclarativeContainer):
    """IoC container of csv application component providers."""

    main = providers.Callable(example.main.main,
                              movie_lister=movies.MoviesModule.movie_lister)

    init_db = providers.Callable(example.db.init_csv,
                                 movies_data=settings.MOVIES_SAMPLE_DATA,
                                 csv_file_path=settings.MOVIES_CSV_PATH,
                                 delimiter=',')


if __name__ == '__main__':
    CsvApplication.init_db()
    CsvApplication.main()
