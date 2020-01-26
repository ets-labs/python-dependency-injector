"""Movie models module.

This module contains all model implementations.
"""


class Movie:
    """Base movie model."""

    def __init__(self, name, year, director):
        """Initialize instance.

        :param name: Movie's name
        :type name: str

        :param year: Year, when movie was released
        :type year: int

        :param director: Name of person, that directed the movie
        :type director: str
        """
        self.name = str(name)
        self.year = int(year)
        self.director = str(director)

    def __repr__(self):
        """Return string representation of movie instance.

        :rtype: str
        :return: Movie's string representation.
        """
        return '{0}(name={1}, year={2}, director={3})'.format(
            self.__class__.__name__,
            repr(self.name),
            repr(self.year),
            repr(self.director))
