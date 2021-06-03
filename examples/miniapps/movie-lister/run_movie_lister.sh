#!/bin/bash -ef

rm -rf wslenv2

python3 -m venv wslenv2
. wslenv2/bin/activate

pip install -r requirements.txt
wslenv2/bin/python data/fixtures.py

MOVIE_FINDER_TYPE=csv wslenv2/bin/python -m movies
MOVIE_FINDER_TYPE=sqlite wslenv2/bin/python -m movies
