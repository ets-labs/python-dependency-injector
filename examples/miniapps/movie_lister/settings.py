"""Settings module.

This module contains application's settings and constants.
"""

import os


DATA_DIR = os.path.abspath(os.path.dirname(__file__) + '/data')
MOVIES_CSV_PATH = DATA_DIR + '/movies.csv'
MOVIES_DB_PATH = DATA_DIR + '/movies.db'

MOVIES_SAMPLE_DATA = (
    ('The Hunger Games: Mockingjay - Part 2', 2015, 'Francis Lawrence'),
    ('The 33', 2015, 'Patricia Riggen'),
    ('Star Wars: Episode VII - The Force Awakens', 2015, 'JJ Abrams'),
)
