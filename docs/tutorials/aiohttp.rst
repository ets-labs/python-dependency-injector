.. _aiohttp-tutorial:

Aiohttp tutorial
================

.. meta::
   :keywords: Python,Aiohttp,Tutorial,Education,Web,API,REST API,Example,DI,Dependency injection,
              IoC,Inversion of control,Refactoring,Tests,Unit tests,Pytest,py.test,Bootstrap,
              HTML,CSS
   :description: This tutorial shows how to build an aiohttp application following the dependency
                 injection principle. You will create the REST API application, connect to the
                 Giphy API, cover it with the unit test and make some refactoring.

This tutorial shows how to build an ``aiohttp`` REST API application following the dependency
injection principle.

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/aiohttp>`_.

What are we going to build?
---------------------------

.. image:: https://media.giphy.com/media/apvx5lPCPsjN6/source.gif

We will build a REST API application that searches for funny GIFs on the `Giphy <https://giphy.com/>`_.
Let's call it Giphy Navigator.

How does Giphy Navigator work?

- Client sends a request specifying the search query and the number of results.
- Giphy Navigator returns a response in json format.
- The response contains:
    - the search query
    - the limit number
    - the list of gif urls

Example response:

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

The task is naive and that's exactly what we need for the tutorial.

Prepare the environment
-----------------------

Let's create the environment for the project.

First we need to create a project folder:

.. code-block:: bash

   mkdir giphynav-aiohttp-tutorial
   cd giphynav-aiohttp-tutorial

Now let's create and activate virtual environment:

.. code-block:: bash

   python3 -m venv venv
   . venv/bin/activate

Environment is ready and now we're going to create the layout of the project.

Project layout
--------------

Create next structure in the current directory. All files should be empty. That's ok for now.

Initial project layout::

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   └── handlers.py
   ├── venv/
   └── requirements.txt

Install the requirements
------------------------

Now it's time to install the project requirements. We will use next packages:

- ``dependency-injector`` - the dependency injection framework
- ``aiohttp`` - the web framework
- ``pyyaml`` - the YAML files parsing library, used for the reading of the configuration files
- ``pytest-aiohttp`` - the helper library for the testing of the ``aiohttp`` application
- ``pytest-cov`` - the helper library for measuring the test coverage

Put next lines into the ``requirements.txt`` file:

.. code-block:: bash

   dependency-injector
   aiohttp
   pyyaml
   pytest-aiohttp
   pytest-cov

and run next in the terminal:

.. code-block:: bash

   pip install -r requirements.txt

Let's also install the ``httpie``. It is a user-friendly command-line HTTP client for the API era.
We will use it for the manual testing.

Run the command in the terminal:

.. code-block:: bash

   pip install httpie

The requirements are setup. Now we will build a minimal application.

Minimal application
-------------------

In this section we will build a minimal application. It will have an endpoint that
will answer our requests in json format. There will be no payload for now.

Edit ``handlers.py``:

.. code-block:: python

   """Handlers module."""

   from aiohttp import web


   async def index(request: web.Request) -> web.Response:
       query = request.query.get("query", "Dependency Injector")
       limit = int(request.query.get("limit", 10))

       gifs = []

       return web.json_response(
           {
               "query": query,
               "limit": limit,
               "gifs": gifs,
           },
       )

Now let's create a container. Container will keep all of the application components and their dependencies.

Edit ``containers.py``:

.. code-block:: python

   """Containers module."""

   from dependency_injector import containers


   class Container(containers.DeclarativeContainer):
       ...

Container is empty for now. We will add the providers in the following sections.

Finally we need to create ``aiohttp`` application factory. It will create and configure container
and ``web.Application``. It is traditionally called ``create_app()``.
We will assign ``index`` handler to handle user requests to the root ``/`` of our web application.

Put next into the ``application.py``:

.. code-block:: python

   """Application module."""

   from aiohttp import web

   from .containers import Container
   from . import handlers


   def create_app() -> web.Application:
       container = Container()

       app = web.Application()
       app.container = container
       app.add_routes([
           web.get("/", handlers.index),
       ])
       return app


   if __name__ == "__main__":
       app = create_app()
       web.run_app(app)

Now we're ready to run our application

Do next in the terminal:

.. code-block:: bash

   python -m giphynavigator.application

The output should be something like:

.. code-block:: bash

   ======== Running on http://0.0.0.0:8080 ========
   (Press CTRL+C to quit)

Let's check that it works. Open another terminal session and use ``httpie``:

.. code-block:: bash

   http http://0.0.0.0:8080/

You should see:

.. code-block:: json

   HTTP/1.1 200 OK
   Content-Length: 844
   Content-Type: application/json; charset=utf-8
   Date: Wed, 29 Jul 2020 21:01:50 GMT
   Server: Python/3.10 aiohttp/3.6.2

   {
       "gifs": [],
       "limit": 10,
       "query": "Dependency Injector"
   }

Minimal application is ready. Let's connect our application with the Giphy API.

Giphy API client
----------------

In this section we will integrate our application with the Giphy API.

We will create our own API client using ``aiohttp`` client.

Create ``giphy.py`` module in the ``giphynavigator`` package:

.. code-block:: bash
   :emphasize-lines: 6

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   └── handlers.py
   ├── venv/
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Giphy client module."""

   from aiohttp import ClientSession, ClientTimeout


   class GiphyClient:

       API_URL = "https://api.giphy.com/v1"

       def __init__(self, api_key, timeout):
           self._api_key = api_key
           self._timeout = ClientTimeout(timeout)

       async def search(self, query, limit):
           """Make search API call and return result."""
           url = f"{self.API_URL}/gifs/search"
           params = {
               "q": query,
               "api_key": self._api_key,
               "limit": limit,
           }
           async with ClientSession(timeout=self._timeout) as session:
               async with session.get(url, params=params) as response:
                   if response.status != 200:
                       response.raise_for_status()
                   return await response.json()

Now we need to add ``GiphyClient`` into the container. The ``GiphyClient`` has two dependencies
that have to be injected: the API key and the request timeout. We will need to use two more
providers from the ``dependency_injector.providers`` module:

- ``Factory`` provider. It will create a ``GiphyClient`` client.
- ``Configuration`` provider. It will provide an API key and a request timeout for the ``GiphyClient``
  client. We will specify the location of the configuration file. The configuration provider will parse
  the configuration file when we create a container instance.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 3-5,10-16

   """Containers module."""

   from dependency_injector import containers, providers

   from . import giphy


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

Now let's add the configuration file. We will use YAML. Create an empty file ``config.yml`` in
the root root of the project:

.. code-block:: bash
   :emphasize-lines: 9

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   └── handlers.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: yaml

   giphy:
     request_timeout: 10


We will use the ``GIPHY_API_KEY`` environment variable to provide the API key. Let’s edit
``create_app()`` to fetch the key value from it.

Edit ``application.py``:

.. code-block:: python
   :emphasize-lines: 11

   """Application module."""

   from aiohttp import web

   from .containers import Container
   from . import handlers


   def create_app() -> web.Application:
       container = Container()
       container.config.giphy.api_key.from_env("GIPHY_API_KEY")

       app = web.Application()
       app.container = container
       app.add_routes([
           web.get("/", handlers.index),
       ])
       return app


   if __name__ == "__main__":
       app = create_app()
       web.run_app(app)

Now we need to create an API key and set it to the environment variable.

As for now, don’t worry, just take this one:

.. code-block:: bash

   export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0

.. note::

   To create your own Giphy API key follow this
   `guide <https://support.giphy.com/hc/en-us/articles/360020283431-Request-A-GIPHY-API-Key>`_.

The Giphy API client and the configuration setup is done. Let's proceed to the search service.

Search service
--------------

Now it's time to add the ``SearchService``. It will:

- Perform the search.
- Format result data.

``SearchService`` will use ``GiphyClient``.

Create ``services.py`` module in the ``giphynavigator`` package:

.. code-block:: bash
   :emphasize-lines: 8

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   ├── handlers.py
   │   └── services.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Services module."""

   from .giphy import GiphyClient


   class SearchService:

       def __init__(self, giphy_client: GiphyClient):
           self._giphy_client = giphy_client

       async def search(self, query, limit):
           """Search for gifs and return formatted data."""
           if not query:
               return []

           result = await self._giphy_client.search(query, limit)

           return [{"url": gif["url"]} for gif in result["data"]]

The ``SearchService`` has a dependency on the ``GiphyClient``. This dependency will be
injected when we add ``SearchService`` to the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 5,18-21

   """Containers module."""

   from dependency_injector import containers, providers

   from . import giphy, services


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

The search service is ready. In next section we're going to put it to work.

Make the search work
--------------------

Now we are ready to put the search into work. Let's inject ``SearchService`` into
the ``index`` handler. We will use :ref:`wiring` feature.

Edit ``handlers.py``:

.. code-block:: python
   :emphasize-lines: 4-7,10-14,18

   """Handlers module."""

   from aiohttp import web
   from dependency_injector.wiring import Provide, inject

   from .services import SearchService
   from .containers import Container


   @inject
   async def index(
           request: web.Request,
           search_service: SearchService = Provide[Container.search_service],
   ) -> web.Response:
       query = request.query.get("query", "Dependency Injector")
       limit = int(request.query.get("limit", 10))

       gifs = await search_service.search(query, limit)

       return web.json_response(
           {
               "query": query,
               "limit": limit,
               "gifs": gifs,
           },
       )

To make the injection work we need to wire the container with the ``handlers`` module.
Let's configure the container to automatically make wiring with the ``handlers`` module when we
create a container instance.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 10

   """Containers module."""

   from dependency_injector import containers, providers

   from . import giphy, services


   class Container(containers.DeclarativeContainer):

       wiring_config = containers.WiringConfiguration(modules=[".handlers"])

       config = providers.Configuration(yaml_files=["config.yml"])

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

Make sure the app is running:

.. code-block:: bash

   python -m giphynavigator.application

and make a request to the API in the terminal:

.. code-block:: bash

   http http://0.0.0.0:8080/ query=="wow,it works" limit==5

You should see:

.. code-block:: json

   HTTP/1.1 200 OK
   Content-Length: 492
   Content-Type: application/json; charset=utf-8
   Date: Fri, 09 Oct 2020 01:35:48 GMT
   Server: Python/3.10 aiohttp/3.6.2

   {
       "gifs": [
           {
               "url": "https://giphy.com/gifs/dollyparton-3xIVVMnZfG3KQ9v4Ye"
           },
           {
               "url": "https://giphy.com/gifs/tennistv-unbelievable-disbelief-cant-believe-UWWJnhHHbpGvZOapEh"
           },
           {
               "url": "https://giphy.com/gifs/discoverychannel-nugget-gold-rush-rick-ness-KGGPIlnC4hr4u2s3pY"
           },
           {
               "url": "https://giphy.com/gifs/soulpancake-wow-work-xUe4HVXTPi0wQ2OAJC"
           },
           {
               "url": "https://giphy.com/gifs/readingrainbow-teamwork-levar-burton-reading-rainbow-3o7qE1EaTWLQGDSabK"
           }
       ],
       "limit": 5,
       "query": "wow,it works"
   }

.. image:: https://media.giphy.com/media/3oxHQCI8tKXoeW4IBq/source.gif

The search works!

Make some refactoring
---------------------

Our ``index`` handler has two hardcoded config values:

- Default search query
- Default results limit

Let's make some refactoring. We will move these values to the config.

Edit ``handlers.py``:

.. code-block:: python
   :emphasize-lines: 14-15,17-18

   """Handlers module."""

   from aiohttp import web
   from dependency_injector.wiring import Provide, inject

   from .services import SearchService
   from .containers import Container


   @inject
   async def index(
           request: web.Request,
           search_service: SearchService = Provide[Container.search_service],
           default_query: str = Provide[Container.config.default.query],
           default_limit: int = Provide[Container.config.default.limit.as_int()],
   ) -> web.Response:
       query = request.query.get("query", default_query)
       limit = int(request.query.get("limit", default_limit))

       gifs = await search_service.search(query, limit)

       return web.json_response(
           {
               "query": query,
               "limit": limit,
               "gifs": gifs,
           },
       )

Let's update the config.

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 3-5

   giphy:
     request_timeout: 10
   default:
     query: "Dependency Injector"
     limit: 10

The refactoring is done. We've made it cleaner - hardcoded values are now moved to the config.

Tests
-----

In this section we will add some tests.

Create ``tests.py`` module in the ``giphynavigator`` package:

.. code-block:: bash
   :emphasize-lines: 9

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   ├── handlers.py
   │   ├── services.py
   │   └── tests.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python
   :emphasize-lines: 32,59,73

   """Tests module."""

   from unittest import mock

   import pytest

   from giphynavigator.application import create_app
   from giphynavigator.giphy import GiphyClient


   @pytest.fixture
   def app():
       app = create_app()
       yield app
       app.container.unwire()


   @pytest.fixture
   def client(app, aiohttp_client, loop):
       return loop.run_until_complete(aiohttp_client(app))


   async def test_index(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           "data": [
               {"url": "https://giphy.com/gif1.gif"},
               {"url": "https://giphy.com/gif2.gif"},
           ],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get(
               "/",
               params={
                   "query": "test",
                   "limit": 10,
               },
           )

       assert response.status == 200
       data = await response.json()
       assert data == {
           "query": "test",
           "limit": 10,
           "gifs": [
               {"url": "https://giphy.com/gif1.gif"},
               {"url": "https://giphy.com/gif2.gif"},
           ],
       }


   async def test_index_no_data(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           "data": [],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get("/")

       assert response.status == 200
       data = await response.json()
       assert data["gifs"] == []


   async def test_index_default_params(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           "data": [],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get("/")

       assert response.status == 200
       data = await response.json()
       assert data["query"] == app.container.config.default.query()
       assert data["limit"] == app.container.config.default.limit()

Now let's run it and check the coverage:

.. code-block:: bash

   py.test giphynavigator/tests.py --cov=giphynavigator

You should see:

.. code-block::

   platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
   plugins: asyncio-0.16.0, anyio-3.3.4, aiohttp-0.3.0, cov-3.0.0
   collected 3 items

   giphynavigator/tests.py ...                                     [100%]

   ---------- coverage: platform darwin, python 3.10.0-final-0 ----------
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   giphynavigator/__init__.py          0      0   100%
   giphynavigator/application.py      13      2    85%
   giphynavigator/containers.py        7      0   100%
   giphynavigator/giphy.py            14      9    36%
   giphynavigator/handlers.py         10      0   100%
   giphynavigator/services.py          9      1    89%
   giphynavigator/tests.py            37      0   100%
   ---------------------------------------------------
   TOTAL                              90     12    87%

.. note::

   Take a look at the highlights in the ``tests.py``.

   It emphasizes the overriding of the ``GiphyClient``. The real API call are mocked.

Conclusion
----------

In this tutorial we've built an ``aiohttp`` REST API application following the dependency
injection principle.
We've used the ``Dependency Injector`` as a dependency injection framework.

:ref:`containers` and :ref:`providers` helped to specify how to assemble search service and
giphy client.

:ref:`configuration-provider` helped to deal with reading YAML file and environment variable.

We used :ref:`wiring` feature to inject the dependencies into the ``index()`` handler.
:ref:`provider-overriding` feature helped in testing.

We kept all the dependencies injected explicitly. This will help when you need to add or
change something in future.

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/aiohttp>`_.

What's next?

- Look at the other :ref:`tutorials`
- Know more about the :ref:`providers`
- Go to the :ref:`contents`

.. include:: ../sponsor.rst

.. disqus::
