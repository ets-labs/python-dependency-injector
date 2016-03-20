"""Movie finders."""

import csv


class MovieFinder(object):
    """Movie finder."""

    def __init__(self, movie_model):
        """Initializer."""
        self.movie_model = movie_model

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):
    """Movie finder that fetches movies info from csv file."""

    def __init__(self, movie_model, csv_file, delimeter):
        """Initializer."""
        self.csv_file = csv_file
        self.delimeter = delimeter
        super(CsvMovieFinder, self).__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        with open(self.csv_file) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimeter)
            return [self.movie_model(*row) for row in reader]


class SqliteMovieFinder(MovieFinder):
    """Movie finder that fetches movies info from sqlite database."""

    def __init__(self, movie_model, database):
        """Initializer."""
        self.database = database
        super(SqliteMovieFinder, self).__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[:py:class:`Movie`]
        :return: List of movie instances.
        """
        with self.database:
            rows = self.database.execute('SELECT name, year, director '
                                         'FROM movies')
            return [self.movie_model(*row) for row in rows]
