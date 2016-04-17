"""Movie listers module.

This module contains all lister implementations.
"""


class MovieLister(object):
    """Movie lister component.

    Movie lister component provides several methods for filtering movies by
    specific criteria.
    """

    def __init__(self, movie_finder):
        """Initializer.

        :param movie_finder: Movie finder instance
        :type movie_finder: movies.finders.MovieFinder
        """
        self._movie_finder = movie_finder

    def movies_directed_by(self, director):
        """Return list of movies that were directed by certain person.

        :param director: Director's name
        :type director: str

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        return [movie for movie in self._movie_finder.find_all()
                if movie.director == director]

    def movies_released_in(self, year):
        """Return list of movies that were released in certain year.

        :param year: Release year
        :type year: int

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        return [movie for movie in self._movie_finder.find_all()
                if movie.year == year]
