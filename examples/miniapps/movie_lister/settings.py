"""Settings module.

This module contains application's settings and constants.
"""

import os


DATA_DIR = os.path.abspath(os.path.dirname(__file__) + '/data')
MOVIES_CSV_PATH = DATA_DIR + '/movies.csv'
MOVIES_DB_PATH = DATA_DIR + '/movies.db'
