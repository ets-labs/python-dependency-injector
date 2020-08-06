Asyncio Daemon Dependency Injection Example
===========================================

Application ``monitoringdaemon`` is an `asyncio <https://docs.python.org/3/library/asyncio.html>`_
+ `Dependency Injector <http://python-dependency-injector.ets-labs.org/>`_ application.

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

   Starting monitoring-daemon-asyncio_monitor_1 ... done
   Attaching to monitoring-daemon-asyncio_monitor_1
   monitor_1  | [2020-08-06 01:57:08,249] [INFO] [monitoringdaemon.dispatcher]: Dispatcher is starting up
   monitor_1  | [2020-08-06 01:57:08,249] [INFO] [monitoringdaemon.dispatcher]: Monitoring task has been started monitoringdaemon.monitors.HttpMonitor(url="http://example.com")
   monitor_1  | [2020-08-06 01:57:08,249] [INFO] [monitoringdaemon.dispatcher]: Monitoring task has been started monitoringdaemon.monitors.HttpMonitor(url="http://httpbin.org/get")
   monitor_1  | [2020-08-06 01:57:08,318] [INFO] [monitoringdaemon.monitors.HttpMonitor(url="http://example.com")]: Response code: 200, content length: 648, request took: 0.067 seconds
   monitor_1  | [2020-08-06 01:57:08,363] [INFO] [monitoringdaemon.monitors.HttpMonitor(url="http://httpbin.org/get")]: Response code: 200, content length: 309, request took: 0.112 seconds

Test
----

This application comes with the unit tests.

To run the tests do:

.. code-block:: bash

   docker-compose run --rm monitor py.test monitoringdaemon/tests.py --cov=monitoringdaemon

The output should be something like:

.. code-block::

   platform linux -- Python 3.8.3, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
   rootdir: /code
   plugins: asyncio-0.14.0, cov-2.10.0
   collected 2 items

   monitoringdaemon/tests.py ..                                     [100%]

   ----------- coverage: platform linux, python 3.8.3-final-0 -----------
   Name                             Stmts   Miss  Cover
   ----------------------------------------------------
   monitoringdaemon/__init__.py         0      0   100%
   monitoringdaemon/__main__.py         9      9     0%
   monitoringdaemon/containers.py      11      0   100%
   monitoringdaemon/dispatcher.py      45      5    89%
   monitoringdaemon/http.py             6      3    50%
   monitoringdaemon/monitors.py        29      2    93%
   monitoringdaemon/tests.py           37      0   100%
   ----------------------------------------------------
   TOTAL                              137     19    86%
