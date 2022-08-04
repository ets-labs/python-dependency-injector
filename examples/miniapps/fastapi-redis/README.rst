FastAPI + Redis + Dependency Injector Example
=============================================

This is a `FastAPI <https://docs.python.org/3/library/asyncio.html>`_
+ `Redis <https://redis.io/>`_
+ `Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application.

Run
---

Build the Docker image:

.. code-block:: bash

   docker-compose build

Run the docker-compose environment:

.. code-block:: bash

    docker-compose up

The output should be something like:

.. code-block::

   redis_1    | 1:C 04 Jan 2022 02:42:14.115 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
   redis_1    | 1:C 04 Jan 2022 02:42:14.115 # Redis version=6.0.9, bits=64, commit=00000000, modified=0, pid=1, just started
   redis_1    | 1:C 04 Jan 2022 02:42:14.115 # Configuration loaded
   redis_1    | 1:M 04 Jan 2022 02:42:14.116 * Running mode=standalone, port=6379.
   redis_1    | 1:M 04 Jan 2022 02:42:14.116 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
   redis_1    | 1:M 04 Jan 2022 02:42:14.116 # Server initialized
   redis_1    | 1:M 04 Jan 2022 02:42:14.117 * Loading RDB produced by version 6.0.9
   redis_1    | 1:M 04 Jan 2022 02:42:14.117 * RDB age 1 seconds
   redis_1    | 1:M 04 Jan 2022 02:42:14.117 * RDB memory usage when created 0.77 Mb
   redis_1    | 1:M 04 Jan 2022 02:42:14.117 * DB loaded from disk: 0.000 seconds
   redis_1    | 1:M 04 Jan 2022 02:42:14.117 * Ready to accept connections
   redis_1    | 1:signal-handler (1609728137) Received SIGTERM scheduling shutdown...
   redis_1    | 1:M 04 Jan 2022 02:42:17.984 # User requested shutdown...
   redis_1    | 1:M 04 Jan 2022 02:42:17.984 # Redis is now ready to exit, bye bye...
   redis_1    | 1:C 04 Jan 2022 02:42:22.035 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
   redis_1    | 1:C 04 Jan 2022 02:42:22.035 # Redis version=6.0.9, bits=64, commit=00000000, modified=0, pid=1, just started
   redis_1    | 1:C 04 Jan 2022 02:42:22.035 # Configuration loaded
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * Running mode=standalone, port=6379.
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 # Server initialized
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * Loading RDB produced by version 6.0.9
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * RDB age 9 seconds
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * RDB memory usage when created 0.77 Mb
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * DB loaded from disk: 0.000 seconds
   redis_1    | 1:M 04 Jan 2022 02:42:22.037 * Ready to accept connections
   example_1  | INFO:     Started server process [1]
   example_1  | INFO:     Waiting for application startup.
   example_1  | INFO:     Application startup complete.
   example_1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

Test
----

This application comes with the unit tests.

To run the tests do:

.. code-block:: bash

   docker-compose run --rm example py.test fastapiredis/tests.py --cov=fastapiredis

The output should be something like:

.. code-block::

   platform linux -- Python 3.9, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
   rootdir: /code
   plugins: cov-2.10.1, asyncio-0.14.0
   collected 1 item

   fastapiredis/tests.py .                                         [100%]

   ----------- coverage: platform linux, python 3.9 -----------
   Name                          Stmts   Miss  Cover
   -------------------------------------------------
   fastapiredis/__init__.py          0      0   100%
   fastapiredis/application.py      15      0   100%
   fastapiredis/containers.py        6      0   100%
   fastapiredis/redis.py             7      4    43%
   fastapiredis/services.py          7      3    57%
   fastapiredis/tests.py            18      0   100%
   -------------------------------------------------
   TOTAL                            53      7    87%
