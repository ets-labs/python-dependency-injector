"""Movies package components."""

import csv


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


class MovieFinder(object):
    """Movie finder."""

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):
    """Movie finder that fetches movies info from csv file."""

    def __init__(self, csv_file, delimeter):
        """Initializer."""
        self.csv_file = csv_file
        self.delimeter = delimeter

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        with open(self.csv_file) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimeter)
            return [Movie(*row) for row in reader]


class SqliteMovieFinder(MovieFinder):
    """Movie finder that fetches movies info from sqlite database."""

    def __init__(self, database):
        """Initializer."""
        self.database = database

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        with self.database:
            rows = self.database.execute('SELECT name, year, director '
                                         'FROM movies')
            return [Movie(*row) for row in rows]


class Movie(object):
    """Movie model."""

    def __init__(self, name, year, director):
        """Initializer."""
        self.name = str(name)
        self.year = int(year)
        self.director = str(director)

    def __repr__(self):
        """Return string representation of movie instance."""
        return 'Movie(name={0}, year={1}, director={2})'.format(
            repr(self.name), repr(self.year), repr(self.director))
