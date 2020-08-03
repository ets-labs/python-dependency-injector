Aiohttp tutorial
================

.. _aiohttp-tutorial:

This tutorials shows how to build an ``aiohttp`` REST API application following the dependency
injection principle.

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/giphynav-aiohttp>`_.

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

First we need to create a project folder and the virtual environment:

.. code-block:: bash

   mkdir giphynav-aiohttp-tutorial
   cd giphynav-aiohttp-tutorial
   python3 -m venv venv

Now let's activate the virtual environment:

.. code-block:: bash

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
   │   └── views.py
   ├── venv/
   └── requirements.txt

Install the requirements
------------------------

Now it's time to install the project requirements. We will use next packages:

- ``dependency-injector`` - the dependency injection framework
- ``aiohttp`` - the web framework
- ``aiohttp-devtools`` - the helper library that will provide a development server with live
  reloading
- ``pyyaml`` - the YAML files parsing library, used for the reading of the configuration files
- ``pytest-aiohttp`` - the helper library for the testing of the ``aiohttp`` application
- ``pytest-cov`` - the helper library for measuring the test coverage

Put next lines into the ``requirements.txt`` file:

.. code-block:: bash

   dependency-injector
   aiohttp
   aiohttp-devtools
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

In this section we will build a minimal application. It will have an endpoint that we can call.
The endpoint will answer in the right format and will have no data.

Edit ``views.py``:

.. code-block:: python

   """Views module."""

   from aiohttp import web


   async def index(request: web.Request) -> web.Response:
       query = request.query.get('query', 'Dependency Injector')
       limit = int(request.query.get('limit', 10))

       gifs = []

       return web.json_response(
           {
               'query': query,
               'limit': limit,
               'gifs': gifs,
           },
       )

Now let's create the main part of our application - the container. Container will keep all of the
application components and their dependencies. First two providers we need to add are
the ``aiohttp`` application provider and the view provider.

Put next into the ``containers.py``:

.. code-block:: python

   """Application containers module."""

   from dependency_injector import containers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       index_view = aiohttp.View(views.index)

At the last we need to create the ``aiohttp`` application factory. It is traditionally called
``create_app()``. It will create the container. Then it will use the container to create
the ``aiohttp`` application. Last step is to configure the routing - we will assign
``index_view`` from the container to handle the requests to the root ``/`` of our REST API server.

Put next into the ``application.py``:

.. code-block:: python

   """Application module."""

   from aiohttp import web

   from .containers import ApplicationContainer


   def create_app():
       """Create and return aiohttp application."""
       container = ApplicationContainer()

       app: web.Application = container.app()
       app.container = container

       app.add_routes([
           web.get('/', container.index_view.as_view()),
       ])

       return app

.. note::

   Container is the first object in the application.

   The container is used to create all other objects.

Now we're ready to run our application

Do next in the terminal:

.. code-block:: bash

   adev runserver giphynavigator/application.py --livereload

The output should be something like:

.. code-block:: bash

   [18:52:59] Starting aux server at http://localhost:8001 ◆
   [18:52:59] Starting dev server at http://localhost:8000 ●

Let's use ``httpie`` to check that it works:

.. code-block:: bash

   http http://127.0.0.1:8000/

You should see:

.. code-block:: json

   HTTP/1.1 200 OK
   Content-Length: 844
   Content-Type: application/json; charset=utf-8
   Date: Wed, 29 Jul 2020 21:01:50 GMT
   Server: Python/3.8 aiohttp/3.6.2

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
   │   └── views.py
   ├── venv/
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Giphy client module."""

   from aiohttp import ClientSession, ClientTimeout


   class GiphyClient:

       API_URL = 'http://api.giphy.com/v1'

       def __init__(self, api_key, timeout):
           self._api_key = api_key
           self._timeout = ClientTimeout(timeout)

       async def search(self, query, limit):
           """Make search API call and return result."""
           url = f'{self.API_URL}/gifs/search'
           params = {
               'q': query,
               'api_key': self._api_key,
               'limit': limit,
           }
           async with ClientSession(timeout=self._timeout) as session:
               async with session.get(url, params=params) as response:
                   if response.status != 200:
                       response.raise_for_status()
                   return await response.json()

Now we need to add ``GiphyClient`` into the container. The ``GiphyClient`` has two dependencies
that have to be injected: the API key and the request timeout. We will need to use two more
providers from the ``dependency_injector.providers`` module:

- ``Factory`` provider that will create the ``GiphyClient`` client.
- ``Configuration`` provider that will provide the API key and the request timeout.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 3,7,15,17-21

   """Application containers module."""

   from dependency_injector import containers, providers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import giphy, views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       config = providers.Configuration()

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       index_view = aiohttp.View(views.index)

.. note::

   We have used the configuration value before it was defined. That's the principle how the
   ``Configuration`` provider works.

   Use first, define later.

Now let's add the configuration file.

We will use YAML.

Create an empty file ``config.yml`` in the root root of the project:

.. code-block:: bash
   :emphasize-lines: 9

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   └── views.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: yaml

   giphy:
     request_timeout: 10

We will use an environment variable ``GIPHY_API_KEY`` to provide the API key.

Now we need to edit ``create_app()`` to make two things when application starts:

- Load the configuration file the ``config.yml``.
- Load the API key from the ``GIPHY_API_KEY`` environment variable.

Edit ``application.py``:

.. code-block:: python
   :emphasize-lines: 11-12

   """Application module."""

   from aiohttp import web

   from .containers import ApplicationContainer


   def create_app():
       """Create and return aiohttp application."""
       container = ApplicationContainer()
       container.config.from_yaml('config.yml')
       container.config.giphy.api_key.from_env('GIPHY_API_KEY')

       app: web.Application = container.app()
       app.container = container

       app.add_routes([
           web.get('/', container.index_view.as_view()),
       ])

       return app

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
   :emphasize-lines: 7

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   ├── services.py
   │   └── views.py
   ├── venv/
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

           return [{'url': gif['url']} for gif in result['data']]

The ``SearchService`` has a dependency on the ``GiphyClient``. This dependency will be injected.
Let's add ``SearchService`` to the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 7,23-26

   """Application containers module."""

   from dependency_injector import containers, providers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import giphy, services, views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       config = providers.Configuration()

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

       index_view = aiohttp.View(views.index)


The search service is ready. In the next section we're going to make it work.

Make the search work
--------------------

Now we are ready to make the search work. Let's use the ``SearchService`` in the ``index`` view.

Edit ``views.py``:

.. code-block:: python
   :emphasize-lines: 5,8-11,15

   """Views module."""

   from aiohttp import web

   from .services import SearchService


   async def index(
           request: web.Request,
           search_service: SearchService,
   ) -> web.Response:
       query = request.query.get('query', 'Dependency Injector')
       limit = int(request.query.get('limit', 10))

       gifs = await search_service.search(query, limit)

       return web.json_response(
           {
               'query': query,
               'limit': limit,
               'gifs': gifs,
           },
       )

Now let's inject the ``SearchService`` dependency into the ``index`` view.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 28-31

   """Application containers module."""

   from dependency_injector import containers, providers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import giphy, services, views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       config = providers.Configuration()

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

       index_view = aiohttp.View(
           views.index,
           search_service=search_service,
       )

Make sure the app is running or use:

.. code-block:: bash

   adev runserver giphynavigator/application.py --livereload

and make a request to the API in the terminal:

.. code-block:: bash

   http http://localhost:8000/ query=="wow,it works" limit==5

You should see:

.. code-block:: json

   HTTP/1.1 200 OK
   Content-Length: 850
   Content-Type: application/json; charset=utf-8
   Date: Wed, 29 Jul 2020 22:22:55 GMT
   Server: Python/3.8 aiohttp/3.6.2

   {
       "gifs": [
           {
               "url": "https://giphy.com/gifs/discoverychannel-nugget-gold-rush-rick-ness-KGGPIlnC4hr4u2s3pY"
           },
           {
               "url": "https://giphy.com/gifs/primevideoin-ll1hyBS2IrUPLE0E71"
           },
           {
               "url": "https://giphy.com/gifs/jackman-works-jackmanworks-l4pTgQoCrmXq8Txlu"
           },
           {
               "url": "https://giphy.com/gifs/cat-massage-at-work-l46CzMaOlJXAFuO3u"
           },
           {
               "url": "https://giphy.com/gifs/everwhatproductions-fun-christmas-3oxHQCI8tKXoeW4IBq"
           },
       ],
       "limit": 10,
       "query": "wow,it works"
   }

.. image:: https://media.giphy.com/media/3oxHQCI8tKXoeW4IBq/source.gif

The search works!

Make some refactoring
---------------------

Our ``index`` view has two hardcoded config values:

- Default search query
- Default results limit

Let's make some refactoring. We will move these values to the config.

Edit ``views.py``:

.. code-block:: python
   :emphasize-lines: 11-12,14-15

   """Views module."""

   from aiohttp import web

   from .services import SearchService


   async def index(
           request: web.Request,
           search_service: SearchService,
           default_query: str,
           default_limit: int,
   ) -> web.Response:
       query = request.query.get('query', default_query)
       limit = int(request.query.get('limit', default_limit))

       gifs = await search_service.search(query, limit)

       return web.json_response(
           {
               'query': query,
               'limit': limit,
               'gifs': gifs,
           },
       )

Now we need to inject these values. Let's update the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 31-32

   """Application containers module."""

   from dependency_injector import containers, providers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import giphy, services, views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       config = providers.Configuration()

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

       index_view = aiohttp.View(
           views.index,
           search_service=search_service,
           default_query=config.search.default_query,
           default_limit=config.search.default_limit,
       )

Finally let's update the config.

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 3-5

   giphy:
     request_timeout: 10
   search:
     default_query: "Dependency Injector"
     default_limit: 10

The refactoring is done. We've made it cleaner - hardcoded values are now moved to the config.

In the next section we will add some tests.

Tests
-----

It would be nice to add some tests. Let's do it.

We will use `pytest <https://docs.pytest.org/en/stable/>`_ and
`coverage <https://coverage.readthedocs.io/>`_.

Create ``tests.py`` module in the ``giphynavigator`` package:

.. code-block:: bash
   :emphasize-lines: 8

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   ├── services.py
   │   ├── tests.py
   │   └── views.py
   ├── venv/
   └── requirements.txt

and put next into it:

.. code-block:: python
   :emphasize-lines: 30,57,71

   """Tests module."""

   from unittest import mock

   import pytest

   from giphynavigator.application import create_app
   from giphynavigator.giphy import GiphyClient


   @pytest.fixture
   def app():
       return create_app()


   @pytest.fixture
   def client(app, aiohttp_client, loop):
       return loop.run_until_complete(aiohttp_client(app))


   async def test_index(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           'data': [
               {'url': 'https://giphy.com/gif1.gif'},
               {'url': 'https://giphy.com/gif2.gif'},
           ],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get(
               '/',
               params={
                   'query': 'test',
                   'limit': 10,
               },
           )

       assert response.status == 200
       data = await response.json()
       assert data == {
           'query': 'test',
           'limit': 10,
           'gifs': [
               {'url': 'https://giphy.com/gif1.gif'},
               {'url': 'https://giphy.com/gif2.gif'},
           ],
       }


   async def test_index_no_data(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           'data': [],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get('/')

       assert response.status == 200
       data = await response.json()
       assert data['gifs'] == []


   async def test_index_default_params(client, app):
       giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
       giphy_client_mock.search.return_value = {
           'data': [],
       }

       with app.container.giphy_client.override(giphy_client_mock):
           response = await client.get('/')

       assert response.status == 200
       data = await response.json()
       assert data['query'] == app.container.config.search.default_query()
       assert data['limit'] == app.container.config.search.default_limit()

Now let's run it and check the coverage:

.. code-block:: bash

   py.test giphynavigator/tests.py --cov=giphynavigator

You should see:

.. code-block:: bash

   platform darwin -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
   plugins: cov-2.10.0, aiohttp-0.3.0, asyncio-0.14.0
   collected 3 items

   giphynavigator/tests.py ...                                     [100%]

   ---------- coverage: platform darwin, python 3.8.3-final-0 -----------
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   giphynavigator/__init__.py          0      0   100%
   giphynavigator/__main__.py          5      5     0%
   giphynavigator/application.py      10      0   100%
   giphynavigator/containers.py       10      0   100%
   giphynavigator/giphy.py            14      9    36%
   giphynavigator/services.py          9      1    89%
   giphynavigator/tests.py            35      0   100%
   giphynavigator/views.py             7      0   100%
   ---------------------------------------------------
   TOTAL                              90     15    83%

.. note::

   Take a look at the highlights in the ``tests.py``.

   It emphasizes the overriding of the ``GiphyClient``. The real API call are mocked.

Conclusion
----------

In this tutorial we've build an ``aiohttp`` REST API application following the dependency
injection principle.
We've used ``Dependency Injector`` as a dependency injection framework.

The benefit you get with the ``Dependency Injector`` is the container. It starts to payoff
when you need to understand or change your application structure. It's easy with the container,
cause you have everything in one place:

.. code-block:: python

   """Application containers module."""

   from dependency_injector import containers, providers
   from dependency_injector.ext import aiohttp
   from aiohttp import web

   from . import giphy, services, views


   class ApplicationContainer(containers.DeclarativeContainer):
       """Application container."""

       app = aiohttp.Application(web.Application)

       config = providers.Configuration()

       giphy_client = providers.Factory(
           giphy.GiphyClient,
           api_key=config.giphy.api_key,
           timeout=config.giphy.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           giphy_client=giphy_client,
       )

       index_view = aiohttp.View(
           views.index,
           search_service=search_service,
           default_query=config.search.default_query,
           default_limit=config.search.default_limit,
       )

What's next?

- Look at the other :ref:`tutorials`.
- Know more about the :ref:`providers`.
- Go to the :ref:`contents`.

.. disqus::
