Asyncio daemon tutorial
=======================

.. _asyncio-daemon-tutorial:

This tutorials shows how to build an ``asyncio`` daemon following the dependency injection
principle.

We will use next tools:

- Python 3.8
- Docker
- Docker-compose

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/monitoring-daemon-asyncio>`_.

What are we going to build?
---------------------------

We will build a monitoring daemon that monitors web services availability.

The daemon will send the requests to the `example.com <http://example.com>`_ and
`httpbin.org <https://httpbin.org>`_ every minute. For each successfully completed
response it will log:

- The response code
- The amount of bytes in the response
- The time took to complete the response

.. image::  asyncio_images/diagram.png

Prerequisites
-------------

We will use `Docker <https://www.docker.com/>`_ and
`docker-compose <https://docs.docker.com/compose/>`_ in this tutorial. Let's check the versions:

.. code-block:: bash

   docker --version
   docker-compose --version

The output should look something like:

.. code-block:: bash

   Docker version 19.03.12, build 48a66213fe
   docker-compose version 1.26.2, build eefe0d31

.. note::

   If you don't have ``Docker`` or ``docker-compose`` you need to install them before proceeding.
   Follow these installation guides:

   - `Install Docker <https://docs.docker.com/get-docker/>`_
   - `Install docker-compose <https://docs.docker.com/compose/install/>`_

The prerequisites are satisfied. Let's get started with the project layout.

Project layout
--------------

Project layout starts with the project folder. It is also called the project root.

Create the project root folder and set it as a working directory:

.. code-block:: bash

   mkdir monitoring-daemon-tutorial
   cd monitoring-daemon-tutorial

Now we need to create the project structure. Create the files and folders following next layout.
All files should be empty for now. We will fill them in later.

Initial project layout:

.. code-block:: bash

   ./
   ├── monitoringdaemon/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── dispatcher.py
   │   └── monitors.py
   ├── config.yml
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt

The project layout is ready. Let's prepare the environment.

Prepare the environment
-----------------------

In this section we are going to prepare the environment.

First, we need to specify the project requirements. We will use next packages:

- ``dependency-injector`` - the dependency injection framework
- ``aiohttp`` - the web framework (we need only http client)
- ``pyyaml`` - the YAML files parsing library, used for the reading of the configuration files
- ``pytest`` - the testing framework
- ``pytest-asyncio`` - the helper library for the testing of the ``asyncio`` application
- ``pytest-cov`` - the helper library for measuring the test coverage

Put next lines into the ``requirements.txt`` file:

.. code-block:: bash

   dependency-injector
   aiohttp
   pyyaml
   pytest
   pytest-asyncio
   pytest-cov

Second, we need to create the ``Dockerfile``. It will describe the daemon's build process and
specify how to run it. We will use ``python:3.8-buster`` as a base image.

Put next lines into the ``Dockerfile`` file:

.. code-block:: bash

   FROM python:3.8-buster

   ENV PYTHONUNBUFFERED=1

   WORKDIR /code
   COPY . /code/

   RUN apt-get install openssl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf ~/.cache

   CMD ["python", "-m", "monitoringdaemon"]

Third, we need to define the container in the docker-compose configuration.

Put next lines into the ``docker-compose.yml`` file:

.. code-block:: yaml

   version: "3.7"

   services:

     monitor:
       build: ./
       image: monitoring-daemon
       volumes:
         - "./:/code"

All is ready. Let's check that the environment is setup properly.

Run in the terminal:

.. code-block:: bash

   docker-compose build

The build process may take a couple of minutes. You should see something like this in the end:

.. code-block:: bash

   Successfully built 5b4ee5e76e35
   Successfully tagged monitoring-daemon:latest

After the build is done run the container:

.. code-block:: bash

   docker-compose up

The output should look like:

.. code-block:: bash

   Creating network "monitoring-daemon-tutorial_default" with the default driver
   Creating monitoring-daemon-tutorial_monitor_1 ... done
   Attaching to monitoring-daemon-tutorial_monitor_1
   monitoring-daemon-tutorial_monitor_1 exited with code 0

The environment is ready. The application does not do any work and just exits with a code ``0``.

Logging and configuration
-------------------------

In this section we will configure the logging and configuration file parsing.

Let's start with the the main part of our application - the container. Container will keep all of
the application components and their dependencies.

First two components that we're going to add are the config object and the provider for
configuring the logging.

Put next lines into the ``containers.py`` file:

.. code-block:: python

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

.. note::

   We have used the configuration value before it was defined. That's the principle how the
   ``Configuration`` provider works.

   Use first, define later.

The configuration file will keep the logging settings.

Put next lines into the ``config.yml`` file:

.. code-block:: yaml

   log:
     level: "INFO"
     format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"

At this point we can create the ``main()`` function. It will start our application.

Put next lines into the ``__main__.py`` file:

.. code-block:: python

    """Main module."""

    from .containers import ApplicationContainer


    def main() -> None:
        """Run the application."""
        container = ApplicationContainer()

        container.config.from_yaml('config.yml')
        container.configure_logging()


    if __name__ == '__main__':
        main()

Dispatcher
----------

Now let's add the dispatcher.

The dispatcher will control a list of the monitoring tasks. It will execute each task according
to the configured schedule. The ``Monitor`` class is the base class for all the monitors. You can
create different monitors subclassing it and implementing the ``check()`` method.

.. image:: asyncio_images/class_1.png

Let's create dispatcher and the monitor base classes.

Edit ``monitors.py``:

.. code-block:: python

   """Monitors module."""

   import logging


   class Monitor:

       def __init__(self, check_every: int) -> None:
           self.check_every = check_every
           self.logger = logging.getLogger(self.__class__.__name__)

       async def check(self) -> None:
           raise NotImplementedError()

Edit ``dispatcher.py``:

.. code-block:: python

   """"Dispatcher module."""

   import asyncio
   import logging
   import signal
   import time
   from typing import List

   from .monitors import Monitor


   class Dispatcher:

       def __init__(self, monitors: List[Monitor]) -> None:
           self._monitors = monitors
           self._monitor_tasks: List[asyncio.Task] = []
           self._logger = logging.getLogger(self.__class__.__name__)
           self._stopping = False

       def run(self) -> None:
           asyncio.run(self.start())

       async def start(self) -> None:
           self._logger.info('Starting up')

           for monitor in self._monitors:
               self._monitor_tasks.append(
                   asyncio.create_task(self._run_monitor(monitor)),
               )

           asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
           asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

           await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

           self.stop()

       def stop(self) -> None:
           if self._stopping:
               return

           self._stopping = True

           self._logger.info('Shutting down')
           for task, monitor in zip(self._monitor_tasks, self._monitors):
               task.cancel()
           self._logger.info('Shutdown finished successfully')

       @staticmethod
       async def _run_monitor(monitor: Monitor) -> None:
           def _until_next(last: float) -> float:
               time_took = time.time() - last
               return monitor.check_every - time_took

           while True:
               time_start = time.time()

               try:
                   await monitor.check()
               except asyncio.CancelledError:
                   break
               except Exception:
                   monitor.logger.exception('Error executing monitor check')

               await asyncio.sleep(_until_next(last=time_start))

.. warning:: REWORK
   Every component that we add must be added to the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 8,23-28

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               # TODO: add monitors
           ),
       )

.. warning:: REWORK
   At the last let's use the dispatcher in the ``main()`` function.

Edit ``__main__.py``:

.. code-block:: python
   :emphasize-lines: 13-14

   """Main module."""

   from .containers import ApplicationContainer


   def main() -> None:
       """Run the application."""
       container = ApplicationContainer()

       container.config.from_yaml('config.yml')
       container.configure_logging()

       dispatcher = container.dispatcher()
       dispatcher.run()


   if __name__ == '__main__':
       main()

Finally let's start the container to check that all works.

Run in the terminal:

.. code-block:: bash

   docker-compose up

The output should look like:

.. code-block:: bash

   Starting monitoring-daemon-tutorial_monitor_1 ... done
   Attaching to monitoring-daemon-tutorial_monitor_1
   monitor_1  | [2020-08-07 21:02:01,361] [INFO] [monitoringdaemon.dispatcher]: Dispatcher is starting up
   monitor_1  | [2020-08-07 21:02:01,364] [INFO] [monitoringdaemon.dispatcher]: Dispatcher is shutting down
   monitor_1  | [2020-08-07 21:02:01,364] [INFO] [monitoringdaemon.dispatcher]: Dispatcher shutting down finished successfully
   monitoring-daemon-tutorial_monitor_1 exited with code 0

Everything works properly. Dispatcher starts up and exits because there are no monitoring tasks.

By the end of this section we have the application skeleton ready. In the next section will will
add first monitoring task.

HTTP monitor
------------

Create ``http.py`` module in the ``monitoringdaemon`` package:

.. code-block:: bash
   :emphasize-lines: 7

   ./
   ├── monitoringdaemon/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── dispatcher.py
   │   ├── http.py
   │   └── monitors.py
   ├── config.yml
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Http client module."""

   from aiohttp import ClientSession, ClientTimeout, ClientResponse


   class HttpClient:

       async def request(self, method: str, url: str, timeout: int) -> ClientResponse:
           async with ClientSession(timeout=ClientTimeout(timeout)) as session:
               async with session.request(method, url) as response:
                   return response

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 8, 23

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import http, dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

       http_client = providers.Factory(http.HttpClient)

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               # TODO: add monitors
           ),
       )

Add the http monitor.

Edit ``monitors.py``:

.. code-block:: python
   :emphasize-lines: 4-5,7,24-58

   """Monitors module."""

   import logging
   import time
   from typing import Dict, Any

   from .http import HttpClient


   class Monitor:

       def __init__(self, check_every: int) -> None:
           self.check_every = check_every
           self.logger = logging.getLogger(self.__class__.__name__)

       async def check(self) -> None:
           raise NotImplementedError()


   class HttpMonitor(Monitor):

       def __init__(
               self,
               http_client: HttpClient,
               options: Dict[str, Any],
       ) -> None:
           self._client = http_client
           self._method = options.pop('method')
           self._url = options.pop('url')
           self._timeout = options.pop('timeout')
           super().__init__(check_every=options.pop('check_every'))

       @property
       def full_name(self) -> str:
           return '{0}.{1}(url="{2}")'.format(__name__, self.__class__.__name__, self._url)

       async def check(self) -> None:
           time_start = time.time()

           response = await self._client.request(
               method=self._method,
               url=self._url,
               timeout=self._timeout,
           )

           time_end = time.time()
           time_took = time_end - time_start

           self.logger.info(
               'Response code: %s, content length: %s, request took: %s seconds',
               response.status,
               response.content_length,
               round(time_took, 3)
           )

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 8,25-29,34

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import http, monitors, dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

       http_client = providers.Factory(http.HttpClient)

       example_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.example,
       )

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               example_monitor,
           ),
       )

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 5-11

   log:
     level: "INFO"
     format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"

   monitors:

     example:
       method: "GET"
       url: "http://example.com"
       timeout: 5
       check_every: 5

Run in the terminal:

.. code-block:: bash

   docker-compose up

You will see:

.. code-block:: bash

   [INFO] [Dispatcher]: Starting up
   [INFO] [HttpMonitor]: GET http://example.com, response code: 200, content length: 648, request took: 0.083 seconds
   [INFO] [HttpMonitor]: GET http://example.com, response code: 200, content length: 648, request took: 0.062 seconds

Add another monitor
-------------------

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 31-35,41

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import http, monitors, dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

       http_client = providers.Factory(http.HttpClient)

       example_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.example,
       )

       httpbin_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.httpbin,
       )

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               example_monitor,
               httpbin_monitor,
           ),
       )

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 13-17

   log:
     level: "INFO"
     format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"

   monitors:

     example:
       method: "GET"
       url: "http://example.com"
       timeout: 5
       check_every: 5

     httpbin:
       method: "GET"
       url: "https://httpbin.org/get"
       timeout: 5
       check_every: 5

Tests
-----

Create ``tests.py`` module in the ``monitoringdaemon`` package:

.. code-block:: bash
   :emphasize-lines: 9

   ./
   ├── monitoringdaemon/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── dispatcher.py
   │   ├── http.py
   │   ├── monitors.py
   │   └── tests.py
   ├── config.yml
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Tests module."""

   import asyncio
   import dataclasses
   from unittest import mock

   import pytest

   from .containers import ApplicationContainer


   @dataclasses.dataclass
   class RequestStub:
       status: int
       content_length: int


   @pytest.fixture
   def container():
       container = ApplicationContainer()
       container.config.from_dict({
           'log': {
               'level': 'INFO',
               'formant': '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
           },
           'monitors': {
               'example': {
                   'method': 'GET',
                   'url': 'http://fake-example.com',
                   'timeout': 1,
                   'check_every': 1,
               },
               'httpbin': {
                   'method': 'GET',
                   'url': 'https://fake-httpbin.org/get',
                   'timeout': 1,
                   'check_every': 1,
               },
           },
       })
       return container


   @pytest.mark.asyncio
   async def test_example_monitor(container, caplog):
       caplog.set_level('INFO')

       http_client_mock = mock.AsyncMock()
       http_client_mock.request.return_value = RequestStub(
           status=200,
           content_length=635,
       )

       with container.http_client.override(http_client_mock):
           example_monitor = container.example_monitor()
           await example_monitor.check()

       assert 'http://fake-example.com' in caplog.text
       assert 'response code: 200' in caplog.text
       assert 'content length: 635' in caplog.text


   @pytest.mark.asyncio
   async def test_dispatcher(container, caplog, event_loop):
       caplog.set_level('INFO')

       example_monitor_mock = mock.AsyncMock()
       httpbin_monitor_mock = mock.AsyncMock()

       with container.example_monitor.override(example_monitor_mock), \
               container.httpbin_monitor.override(httpbin_monitor_mock):

           dispatcher = container.dispatcher()
           event_loop.create_task(dispatcher.start())
           await asyncio.sleep(0.1)
           dispatcher.stop()

       assert example_monitor_mock.check.called
       assert httpbin_monitor_mock.check.called

Run in the terminal:

.. code-block:: bash

   docker-compose run --rm monitor py.test monitoringdaemon/tests.py --cov=monitoringdaemon

You should see:

.. code-block:: bash

   platform linux -- Python 3.8.3, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
   rootdir: /code
   plugins: asyncio-0.14.0, cov-2.10.0
   collected 2 items

   monitoringdaemon/tests.py ..                                    [100%]

   ----------- coverage: platform linux, python 3.8.3-final-0 -----------
   Name                             Stmts   Miss  Cover
   ----------------------------------------------------
   monitoringdaemon/__init__.py         0      0   100%
   monitoringdaemon/__main__.py         9      9     0%
   monitoringdaemon/containers.py      11      0   100%
   monitoringdaemon/dispatcher.py      43      5    88%
   monitoringdaemon/http.py             6      3    50%
   monitoringdaemon/monitors.py        23      1    96%
   monitoringdaemon/tests.py           37      0   100%
   ----------------------------------------------------
   TOTAL                              129     18    86%

Conclusion
----------

In this tutorial we've built an ``asyncio`` monitoring daemon  following the dependency
injection principle.
We've used the ``Dependency Injector`` as a dependency injection framework.

The benefit you get with the ``Dependency Injector`` is the container. It starts to payoff
when you need to understand or change your application structure. It's easy with the container,
cause you have everything in one place:

.. code-block:: python

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import http, monitors, dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       config = providers.Configuration()

       configure_logging = providers.Callable(
           logging.basicConfig,
           stream=sys.stdout,
           level=config.log.level,
           format=config.log.format,
       )

       http_client = providers.Factory(http.HttpClient)

       example_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.example,
       )

       httpbin_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.httpbin,
       )

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               example_monitor,
               httpbin_monitor,
           ),
       )

What's next?

- Look at the other :ref:`tutorials`.
- Know more about the :ref:`providers`.
- Go to the :ref:`contents`.

.. disqus::
