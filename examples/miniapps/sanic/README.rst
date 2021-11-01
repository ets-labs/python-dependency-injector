Sanic + Dependency Injector Example
===================================

This is a `Sanic <https://sanic.readthedocs.io/en/latest/index.html>`_ +
`Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application.

The example application is a REST API that searches for funny GIFs on the `Giphy <https://giphy.com/>`_.

Run
---

Create virtual environment:

.. code-block:: bash

   virtualenv venv
   . venv/bin/activate

Install requirements:

.. code-block:: bash

    pip install -r requirements.txt

To run the application do:

.. code-block:: bash

    export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0
    python -m giphynavigator

The output should be something like:

.. code-block::

   [2020-09-23 18:16:31 -0400] [48258] [INFO] Goin' Fast @ http://0.0.0.0:8000
   [2020-09-23 18:16:31 -0400] [48258] [INFO] Starting worker [48258]

After that visit http://127.0.0.1:8000/ in your browser or use CLI command (``curl``, ``httpie``,
etc). You should see something like:

.. code-block:: json

   {
       "query": "Dependency Injector",
       "limit": 10,
       "gifs": [
           {
               "url": "https://giphy.com/gifs/boxes-dependent-swbf2-6Eo7KzABxgJMY"
           },
           {
               "url": "https://giphy.com/gifs/depends-J56qCcOhk6hKE"
           },
           {
               "url": "https://giphy.com/gifs/web-series-ccstudios-bro-dependent-1lhU8KAVwmVVu"
           },
           {
               "url": "https://giphy.com/gifs/TheBoysTV-friends-friend-weneedeachother-XxR9qcIwcf5Jq404Sx"
           },
           {
               "url": "https://giphy.com/gifs/netflix-a-series-of-unfortunate-events-asoue-9rgeQXbwoK53pcxn7f"
           },
           {
               "url": "https://giphy.com/gifs/black-and-white-sad-skins-Hs4YzLs2zJuLu"
           },
           {
               "url": "https://giphy.com/gifs/always-there-for-you-i-am-here-PlayjhCco9jHBYrd9w"
           },
           {
               "url": "https://giphy.com/gifs/stream-famous-dollar-YT2dvOByEwXCdoYiA1"
           },
           {
               "url": "https://giphy.com/gifs/i-love-you-there-for-am-1BhGzgpZXYWwWMAGB1"
           },
           {
               "url": "https://giphy.com/gifs/life-like-twerk-9hlnWxjHqmH28"
           }
       ]
   }

.. note::

   To create your own Giphy API key follow this
   `guide <https://support.giphy.com/hc/en-us/articles/360020283431-Request-A-GIPHY-API-Key>`_.

Test
----

This application comes with the unit tests.

To run the tests do:

.. code-block:: bash

   py.test giphynavigator/tests.py --cov=giphynavigator

The output should be something like:

.. code-block::

   platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
   plugins: sanic-1.9.1, anyio-3.3.4, cov-3.0.0
   collected 3 items

   giphynavigator/tests.py ...                                     [100%]

   ---------- coverage: platform darwin, python 3.10.0-final-0 ----------
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   giphynavigator/__init__.py          0      0   100%
   giphynavigator/__main__.py          4      4     0%
   giphynavigator/application.py      10      0   100%
   giphynavigator/containers.py        7      0   100%
   giphynavigator/giphy.py            14      9    36%
   giphynavigator/handlers.py         11      0   100%
   giphynavigator/services.py          9      1    89%
   giphynavigator/tests.py            39      0   100%
   ---------------------------------------------------
   TOTAL                              94     14    85%
