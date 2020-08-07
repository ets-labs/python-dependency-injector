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
           self.logger = logging.getLogger(self.full_name)

       @property
       def full_name(self) -> str:
           raise NotImplementedError()

       async def check(self) -> None:
           raise NotImplementedError()

Edit ``dispatcher.py``:

.. code-block:: python

   """Dispatcher module."""

   import asyncio
   import logging
   import signal
   import time
   from typing import List

   from .monitors import Monitor


   logger = logging.getLogger(__name__)


   class Dispatcher:

       def __init__(self, monitors: List[Monitor]) -> None:
           self._monitors = monitors
           self._monitor_tasks: List[asyncio.Task] = []
           self._stopping = False

       def run(self) -> None:
           asyncio.run(self.start())

       async def start(self) -> None:
           logger.info('Dispatcher is starting up')

           for monitor in self._monitors:
               self._monitor_tasks.append(
                   asyncio.create_task(self._run_monitor(monitor)),
               )
               logger.info(
                   'Monitoring task has been started %s',
                   monitor.full_name,
               )

           asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
           asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

           await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

           self.stop()

       def stop(self) -> None:
           if self._stopping:
               return

           self._stopping = True

           logger.info('Dispatcher is shutting down')
           for task, monitor in zip(self._monitor_tasks, self._monitors):
               task.cancel()
               logger.info('Monitoring task has been stopped %s', monitor.full_name)
           logger.info('Dispatcher shutting down finished successfully')

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
                   monitor.logger.exception('Error running monitoring check')

               await asyncio.sleep(_until_next(last=time_start))

.. warning:: REWORK
   Every component that we add must be added to the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 8,22-27

   """Application containers module."""

   import logging
   import sys

   from dependency_injector import containers, providers

   from . import dispatcher


   class ApplicationContainer(containers.DeclarativeContainer):

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

Add another monitor
-------------------

Tests
-----

Conclusion
----------

.. disqus::
