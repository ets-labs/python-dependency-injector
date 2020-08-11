"""Movie storages module."""

import csv
import sqlite3
from typing import List, Tuple, Any

Row = Tuple[Any]


class MovieStorage:

    def load_all(self, movie_data: List[Row]):
        raise NotImplementedError()

    def get_all(self) -> List[Row]:
        raise NotImplementedError()


class CsvMovieStorage(MovieStorage):

    def __init__(self, options) -> None:
        self._csv_file_path = options.pop('path')
        self._delimiter = options.pop('delimiter')

    def load_all(self, movie_data: List[Row]) -> None:
        with open(self._csv_file_path, 'w') as csv_file:
            csv.writer(csv_file, delimiter=self._delimiter).writerows(movie_data)

    def get_all(self) -> List[Row]:
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [row for row in csv_reader]


class SqliteMovieStorage(MovieStorage):

    def __init__(self, options) -> None:
        self._database = sqlite3.connect(database=options.pop('path'))

    def load_all(self, movie_data: List[Row]) -> None:
        with self._database as db:
            db.execute(
                'CREATE TABLE IF NOT EXISTS movies '
                '(name text, year int, director text)',
            )
            db.execute('DELETE FROM movies')
            db.executemany('INSERT INTO movies VALUES (?,?,?)', movie_data)

    def get_all(self) -> List[Row]:
        with self._database as db:
            rows = db.execute(
                'SELECT name, year, director '
                'FROM movies',
            )
            return [row for row in rows]
