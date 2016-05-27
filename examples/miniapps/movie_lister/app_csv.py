"""A naive example of dependency injection on Python.

Example implementation of dependency injection in Python from Martin Fowler's
article about dependency injection and inversion of control:

http://www.martinfowler.com/articles/injection.html

This mini application uses ``movies`` library, that is configured to work with
csv file movies database.
"""

from dependency_injector import containers
from dependency_injector import providers
from dependency_injector import injections

from movies import MoviesModule
from movies import finders

from settings import MOVIES_CSV_PATH


@containers.override(MoviesModule)
class MyMoviesModule(containers.DeclarativeContainer):
    """IoC container for overriding movies module component providers."""

    movie_finder = providers.Factory(finders.CsvMovieFinder,
                                     movie_model=MoviesModule.movie_model,
                                     csv_file=MOVIES_CSV_PATH,
                                     delimeter=',')


@injections.inject(MoviesModule.movie_lister)
def main(movie_lister):
    """Main function.

    This program prints info about all movies that were directed by different
    persons and then prints all movies that were released in 2015.

    :param movie_lister: Movie lister instance
    :type movie_lister: movies.listers.MovieLister
    """
    print movie_lister.movies_directed_by('Francis Lawrence')
    print movie_lister.movies_directed_by('Patricia Riggen')
    print movie_lister.movies_directed_by('JJ Abrams')

    print movie_lister.movies_released_in(2015)


if __name__ == '__main__':
    main()
