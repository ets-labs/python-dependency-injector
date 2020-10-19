Asyncio Daemon + Dependency Injector Example
============================================

This is an `asyncio <https://docs.python.org/3/library/asyncio.html>`_ +
`Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application.

The example application is a daemon that monitors availability of web services.

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
   monitor_1  | [2020-08-08 17:04:36,655] [INFO] [Dispatcher]: Starting up
   monitor_1  | [2020-08-08 17:04:36,732] [INFO] [HttpMonitor]: Check
   monitor_1  |     GET http://example.com
   monitor_1  |     response code: 200
   monitor_1  |     content length: 648
   monitor_1  |     request took: 0.074 seconds
   monitor_1  | [2020-08-08 17:04:36,811] [INFO] [HttpMonitor]: Check
   monitor_1  |     GET https://httpbin.org/get
   monitor_1  |     response code: 200
   monitor_1  |     content length: 310
   monitor_1  |     request took: 0.153 seconds
   monitor_1  | [2020-08-08 17:04:41,731] [INFO] [HttpMonitor]: Check
   monitor_1  |     GET http://example.com
   monitor_1  |     response code: 200
   monitor_1  |     content length: 648
   monitor_1  |     request took: 0.067 seconds
   monitor_1  | [2020-08-08 17:04:41,787] [INFO] [HttpMonitor]: Check
   monitor_1  |     GET https://httpbin.org/get
   monitor_1  |     response code: 200
   monitor_1  |     content length: 310
   monitor_1  |     request took: 0.122 seconds
   monitor_1  |

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

   monitoringdaemon/tests.py ..                                    [100%]

   ----------- coverage: platform linux, python 3.8.3-final-0 -----------
   Name                             Stmts   Miss  Cover
   ----------------------------------------------------
   monitoringdaemon/__init__.py         0      0   100%
   monitoringdaemon/__main__.py        12     12     0%
   monitoringdaemon/containers.py      11      0   100%
   monitoringdaemon/dispatcher.py      44      5    89%
   monitoringdaemon/http.py             6      3    50%
   monitoringdaemon/monitors.py        23      1    96%
   monitoringdaemon/tests.py           37      0   100%
   ----------------------------------------------------
   TOTAL                              133     21    84%
