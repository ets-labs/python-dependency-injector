"""Fixtures module."""

import csv
import sqlite3
import pathlib


SAMPLE_DATA = [
    ("The Hunger Games: Mockingjay - Part 2", 2015, "Francis Lawrence"),
    ("Rogue One: A Star Wars Story", 2016, "Gareth Edwards"),
    ("The Jungle Book", 2016, "Jon Favreau"),
]

FILE = pathlib.Path(__file__)
DIR = FILE.parent
CSV_FILE = DIR / "movies.csv"
SQLITE_FILE = DIR / "movies.db"


def create_csv(movies_data, path):
    with open(path, "w", newline="") as opened_file:
        writer = csv.writer(opened_file)
        writer.writerows(movies_data)


def create_sqlite(movies_data, path):
    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS movies "
            "(title text, year int, director text)"
        )
        db.execute("DELETE FROM movies")
        db.executemany("INSERT INTO movies VALUES (?,?,?)", movies_data)


def main():
    create_csv(SAMPLE_DATA, CSV_FILE)
    create_sqlite(SAMPLE_DATA, SQLITE_FILE)
    print("OK")


if __name__ == "__main__":
    main()
