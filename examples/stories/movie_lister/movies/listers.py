"""Movie listers."""


class MovieLister(object):
    """Movie lister."""

    def __init__(self, movie_finder):
        """Initializer."""
        self.movie_finder = movie_finder

    def movies_directed_by(self, director):
        """Return list of movies that were directed by certain person.

        :param director: Director's name
        :type director: str

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        return [movie for movie in self.movie_finder.find_all()
                if movie.director == director]

    def movies_released_in(self, year):
        """Return list of movies that were released in certain year.

        :param year: Release year
        :type year: int

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        return [movie for movie in self.movie_finder.find_all()
                if movie.year == year]
