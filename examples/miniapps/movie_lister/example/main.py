"""Example main module."""


def main(movie_lister):
    """Main function.

    This program prints info about all movies that were directed by different
    persons and then prints all movies that were released in 2015.

    :param movie_lister: Movie lister instance
    :type movie_lister: movies.listers.MovieLister
    """
    print(movie_lister.movies_directed_by('Francis Lawrence'))
    print(movie_lister.movies_directed_by('Patricia Riggen'))
    print(movie_lister.movies_directed_by('JJ Abrams'))

    print(movie_lister.movies_released_in(2015))
