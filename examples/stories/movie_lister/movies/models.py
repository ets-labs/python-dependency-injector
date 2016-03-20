"""Movie models."""


class Movie(object):
    """Movie model."""

    def __init__(self, name, year, director):
        """Initializer."""
        self.name = str(name)
        self.year = int(year)
        self.director = str(director)

    def __repr__(self):
        """Return string representation of movie instance."""
        return '{0}(name={1}, year={2}, director={3})'.format(
            self.__class__.__name__,
            repr(self.name),
            repr(self.year),
            repr(self.director))
