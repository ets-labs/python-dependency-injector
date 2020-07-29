Aiohttp tutorial
================

.. _aiohttp-tutorial:

This tutorials shows how to build ``Aiohttp`` REST API application following dependency injection
principle.

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
- ``pytest-aiohttp``- the helper library for the testing of the ``aiohttp`` application
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
       """Create and return Flask application."""
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
           if not query:
               return []

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
       """Create and return Flask application."""
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

   http http://localhost:8000/ query=="wow,it works"

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
           {
               "url": "https://giphy.com/gifs/spacestationgaming-love-wow-team-YST1F1J5g2yyLLvMJc"
           },
           {
               "url": "https://giphy.com/gifs/dollyparton-3xIVVMnZfG3KQ9v4Ye"
           },
           {
               "url": "https://giphy.com/gifs/greatbigstory-wow-omg-BLGlU7OWvFAFMoNjsM"
           },
           {
               "url": "https://giphy.com/gifs/soulpancake-wow-work-xUe4HVXTPi0wQ2OAJC"
           },
           {
               "url": "https://giphy.com/gifs/nickelodeon-nick-pull-ups-casagrandes-eK136cynbxuOVk0qzJ"
           }
       ],
       "limit": 10,
       "query": "wow,it works"
   }

.. image:: https://media.giphy.com/media/3oxHQCI8tKXoeW4IBq/source.gif

The search works!

Make some refactoring
---------------------

Tests
-----

Conclusion
----------

.. disqus::
