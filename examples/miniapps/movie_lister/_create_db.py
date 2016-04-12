"""Small script for initializing movies data."""

import os
import csv
import sqlite3
import shutil

from settings import DATA_DIR
from settings import MOVIES_CSV_PATH
from settings import MOVIES_DB_PATH


MOVIES = (('The Hunger Games: Mockingjay - Part 2', 2015, 'Francis Lawrence'),
          ('The 33', 2015, 'Patricia Riggen'),
          ('Star Wars: Episode VII - The Force Awakens', 2015, 'JJ Abrams'))


if __name__ == '__main__':
    # (Re)create data directory:
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(DATA_DIR)

    # Initialize sqlite database:
    connection = sqlite3.connect(MOVIES_DB_PATH)
    with connection:
        connection.execute('CREATE TABLE movies '
                           '(name text, year int, director text)')
        connection.executemany('INSERT INTO movies VALUES (?,?,?)', MOVIES)

    # Initialize csv database:
    with open(MOVIES_CSV_PATH, 'w') as csv_file:
        csv.writer(csv_file).writerows(MOVIES)
