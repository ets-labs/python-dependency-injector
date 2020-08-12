"""Movie module."""


class Movie:

    def __init__(self, name: str, year: int, director: str):
        self.name = str(name)
        self.year = int(year)
        self.director = str(director)

    def __repr__(self):
        return '{0}(name={1}, year={2}, director={3})'.format(
            self.__class__.__name__,
            repr(self.name),
            repr(self.year),
            repr(self.director),
        )
