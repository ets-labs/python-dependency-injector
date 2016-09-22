"""Example database module."""

import csv


def init_sqlite(movies_data, database):
    """Initialize sqlite3 movies database.

    :param movies_data: Data about movies
    :type movies_data: tuple[tuple]

    :param database: Connection to sqlite database with movies data
    :type database: sqlite3.Connection
    """
    with database:
        database.execute('CREATE TABLE IF NOT EXISTS movies '
                         '(name text, year int, director text)')
        database.execute('DELETE FROM movies')
        database.executemany('INSERT INTO movies VALUES (?,?,?)', movies_data)


def init_csv(movies_data, csv_file_path, delimiter):
    """Initialize csv movies database.

    :param movies_data: Data about movies
    :type movies_data: tuple[tuple]

    :param csv_file_path: Path to csv file with movies data
    :type csv_file_path: str

    :param delimiter: Csv file's delimiter
    :type delimiter: str
    """
    with open(csv_file_path, 'w') as csv_file:
        csv.writer(csv_file, delimiter=delimiter).writerows(movies_data)
