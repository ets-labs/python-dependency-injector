.. _flask-tutorial:

Flask tutorial
==============

.. meta::
   :keywords: Python,Flask,Tutorial,Education,Web,Example,DI,Dependency injection,IoC,
              Inversion of control,Refactoring,Tests,Unit tests,Pytest,py.test,Bootstrap,
              HTML,CSS
   :description: This tutorial shows how to build a Flask application following the dependency
                 injection principle. You will create the web application, connect to the Github
                 API, cover it with unit the test and make some refactoring.

This tutorial shows how to build a ``Flask`` application following the dependency injection
principle.

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask>`_.

What are we going to build?
---------------------------

We will build a web application that helps to search for repositories on the Github. Let's call it
Github Navigator.

How does Github Navigator work?

- User opens a web page that asks to provide a search query.
- User types the query and hits Enter.
- Github Navigator takes that and searches through the Github for matching repositories.
- When search is done Github Navigator returns user a web page with the result.
- The results page shows all matching repositories and the provided search query.
- For any matching repository user sees:
    - the repository name
    - the owner of the repository
    - the last commit to the repository
- User can click on the repository, the repository owner or the last commit to open its web page
  on the Github.

.. image::  flask-images/screen-02.png

Prepare the environment
-----------------------

Let's create the environment for the project.

First we need to create a project folder:

.. code-block:: bash

   mkdir ghnav-flask-tutorial
   cd ghnav-flask-tutorial

Now let's create and activate virtual environment:

.. code-block:: bash

   python3 -m venv venv
   . venv/bin/activate

Project layout
--------------

Environment is ready and now we're going to create the layout of the project.

Create next structure in the current directory. All files should be empty. That's ok for now.

Initial project layout::

   ./
   ├── githubnavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   └── views.py
   ├── venv/
   └── requirements.txt

Now it's time to install ``Flask`` and ``Dependency Injector``.

Put next lines into the ``requirements.txt`` file:

.. code-block:: bash

   dependency-injector
   flask

Now let's install it:

.. code-block:: bash

   pip install -r requirements.txt

And check that installation is successful:

.. code-block:: bash

   python -c "import dependency_injector; print(dependency_injector.__version__)"
   python -c "import flask; print(flask.__version__)"


You should see something like:

.. code-block:: bash

   (venv) $ python -c "import dependency_injector; print(dependency_injector.__version__)"
   4.37.0
   (venv) $ python -c "import flask; print(flask.__version__)"
   2.0.2

*Versions can be different. That's fine.*

Hello World!
------------

Let's create minimal application.

Put next into the ``views.py``:

.. code-block:: python

   """Views module."""


   def index():
       return "Hello, World!"

Ok, we have the view.

Now let's create a container. Container will keep all of the application components and their dependencies.

Edit ``containers.py``:

.. code-block:: python

   """Containers module."""

   from dependency_injector import containers


   class Container(containers.DeclarativeContainer):
       ...

Container is empty for now. We will add the providers in the following sections.

Finally we need to create Flask application factory. It will create and configure container
and Flask application. It is traditionally called ``create_app()``.
We will assign ``index`` view to handle user requests to the root ``/`` of our web application.

Put next into the ``application.py``:

.. code-block:: python

   """Application module."""

   from flask import Flask

   from .containers import Container
   from . import views


   def create_app() -> Flask:
       container = Container()

       app = Flask(__name__)
       app.container = container
       app.add_url_rule("/", "index", views.index)

       return app

Ok. Now we're ready to say "Hello, World!".

Do next in the terminal:

.. code-block:: bash

   export FLASK_APP=githubnavigator.application
   export FLASK_ENV=development
   flask run

The output should be something like:

.. code-block:: bash

    * Serving Flask app "githubnavigator.application" (lazy loading)
    * Environment: development
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with fsevents reloader
    * Debugger is active!
    * Debugger PIN: 473-587-859

Open your browser and go to the ``http://127.0.0.1:5000/``.

You should see ``Hello, World!``.

That's it. Our minimal application is up and running.

Make it pretty
--------------

Now let's make it look pretty. We will use `Bootstrap 4 <https://getbootstrap.com/>`_.
For adding it to our application we will get
`Bootstrap-Flask <https://pypi.org/project/Bootstrap-Flask/>`_ extension.
It will help us to add all needed static files in few clicks.

Add ``bootstrap-flask`` to the ``requirements.txt``:

.. code-block:: bash
   :emphasize-lines: 3

   dependency-injector
   flask
   bootstrap-flask

and run in the terminal:

.. code-block:: bash

   pip install -r requirements.txt

Let's initialize ``bootstrap-flask`` extension. We will need to modify ``create_app()``.

Edit ``application.py``:

.. code-block:: python
   :emphasize-lines: 4,17-18

   """Application module."""

   from flask import Flask
   from flask_bootstrap import Bootstrap

   from .containers import Container
   from . import views


   def create_app() -> Flask:
       container = Container()

       app = Flask(__name__)
       app.container = container
       app.add_url_rule("/", "index", views.index)

       bootstrap = Bootstrap()
       bootstrap.init_app(app)

       return app

Now we need to add the templates. For doing this we will need to add the folder ``templates/`` to
the ``githubnavigator`` package. We also will need two files there:

- ``base.html`` - the layout
- ``index.html`` - the main page

Create ``templates`` folder and put two empty files into it ``base.html`` and ``index.html``:

.. code-block:: bash
   :emphasize-lines: 3-5

   ./
   ├── githubnavigator/
   │   ├── templates/
   │   │   ├── base.html
   │   │   └── index.html
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   └── views.py
   ├── venv/
   └── requirements.txt

Now let's fill in the layout.

Put next into the ``base.html``:

.. code-block:: html

   <!doctype html>
   <html lang="en">
       <head>
           {% block head %}
           <!-- Required meta tags -->
           <meta charset="utf-8">
           <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

           {% block styles %}
               <!-- Bootstrap CSS -->
               {{ bootstrap.load_css() }}
           {% endblock %}

           <title>{% block title %}{% endblock %}</title>
           {% endblock %}
       </head>
       <body>
           <!-- Your page content -->
           {% block content %}{% endblock %}

           {% block scripts %}
               <!-- Optional JavaScript -->
               {{ bootstrap.load_js() }}
           {% endblock %}
       </body>
   </html>

And put something to the index page.

Put next into the ``index.html``:

.. code-block:: html

   {% extends "base.html" %}

   {% block title %}Github Navigator{% endblock %}

   {% block content %}
   <div class="container">
       <h1 class="mb-4">Github Navigator</h1>

       <form>
           <div class="form-group form-row">
               <div class="col-10">
                   <label for="search_query" class="col-form-label">
                       Search for:
                   </label>
                   <input class="form-control" type="text" id="search_query"
                          placeholder="Type something to search on the GitHub"
                          name="query"
                          value="{{ query if query }}">
               </div>
               <div class="col">
                   <label for="search_limit" class="col-form-label">
                       Limit:
                   </label>
                   <select class="form-control" id="search_limit" name="limit">
                       {% for value in [5, 10, 20] %}
                       <option {% if value == limit %}selected{% endif %}>
                           {{ value }}
                       </option>
                       {% endfor %}
                   </select>
               </div>
           </div>
       </form>

       <p><small>Results found: {{ repositories|length }}</small></p>

       <table class="table table-striped">
           <thead>
               <tr>
                   <th>#</th>
                   <th>Repository</th>
                   <th class="text-nowrap">Repository owner</th>
                   <th class="text-nowrap">Last commit</th>
               </tr>
           </thead>
           <tbody>
           {% for repository in repositories %} {{n}}
               <tr>
                 <th>{{ loop.index }}</th>
                 <td><a href="{{ repository.url }}">
                     {{ repository.name }}</a>
                 </td>
                 <td><a href="{{ repository.owner.url }}">
                     <img src="{{ repository.owner.avatar_url }}"
                          alt="avatar" height="24" width="24"/></a>
                     <a href="{{ repository.owner.url }}">
                         {{ repository.owner.login }}</a>
                 </td>
                 <td><a href="{{ repository.latest_commit.url }}">
                     {{ repository.latest_commit.sha }}</a>
                     {{ repository.latest_commit.message }}
                     {{ repository.latest_commit.author_name }}
                 </td>
               </tr>
           {% endfor %}
           </tbody>
       </table>
   </div>

   {% endblock %}

Ok, almost there. The last step is to make ``index`` view to render the ``index.html`` template.

Edit ``views.py``:

.. code-block:: python

   """Views module."""

   from flask import request, render_template


   def index():
       query = request.args.get("query", "Dependency Injector")
       limit = request.args.get("limit", 10, int)

       repositories = []

       return render_template(
           "index.html",
           query=query,
           limit=limit,
           repositories=repositories,
       )

That's it.

Make sure the app is running or use ``flask run`` and open ``http://127.0.0.1:5000/``.

You should see:

.. image::  flask-images/screen-01.png

Connect to the GitHub
---------------------

In this section we will integrate our application with Github API.

We will use `PyGithub <https://github.com/PyGithub/PyGithub>`_ library for working with Github API.

Let's add it to the ``requirements.txt``:

.. code-block:: bash
   :emphasize-lines: 4

   dependency-injector
   flask
   bootstrap-flask
   pygithub

and run in the terminal:

.. code-block:: bash

   pip install -r requirements.txt

Now we need to add Github API client the container. We will need to add two more providers from
the ``dependency_injector.providers`` module:

- ``Factory`` provider. It will create a ``Github`` client.
- ``Configuration`` provider. It will provide an API token and a request timeout for the ``Github`` client.
  We will specify the location of the configuration file. The configuration provider will parse
  the configuration file when we create a container instance.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 3-4,9,11-15

   """Containers module."""

   from dependency_injector import containers, providers
   from github import Github


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       github_client = providers.Factory(
           Github,
           login_or_token=config.github.auth_token,
           timeout=config.github.request_timeout,
       )


.. note::

   Don't forget to remove the Ellipsis ``...`` from the container. We don't need it anymore
   since we container is not empty.

Now let's add the configuration file. We will use YAML. Create an empty file ``config.yml``
in the root of the project:

.. code-block:: bash
   :emphasize-lines: 11

   ./
   ├── githubnavigator/
   │   ├── templates/
   │   │   ├── base.html
   │   │   └── index.html
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   └── views.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: yaml

   github:
     request_timeout: 10

We will use `PyYAML <https://pypi.org/project/PyYAML/>`_ library for parsing the configuration
file. Let's add it to the requirements file.

Edit ``requirements.txt``:

.. code-block:: bash
   :emphasize-lines: 5

   dependency-injector
   flask
   bootstrap-flask
   pygithub
   pyyaml

and install it:

.. code-block:: bash

   pip install -r requirements.txt

We will use the ``GITHUB_TOKEN`` environment variable to provide the API token. Let's edit
``create_app()`` to fetch the token value from it.

Edit ``application.py``:

.. code-block:: python
   :emphasize-lines: 12

   """Application module."""

   from flask import Flask
   from flask_bootstrap import Bootstrap

   from .containers import Container
   from . import views


   def create_app() -> Flask:
       container = Container()
       container.config.github.auth_token.from_env("GITHUB_TOKEN")

       app = Flask(__name__)
       app.container = container
       app.add_url_rule("/", "index", views.index)

       bootstrap = Bootstrap()
       bootstrap.init_app(app)

       return app

Now we need create an API token.

As for now, don't worry, just take this one:

.. code-block:: bash

   export GITHUB_TOKEN=cbde697a6e01424856fde2b7f94a88d1b501320e

.. note::

   To create your own token:

   - Follow the `Github guide <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_.
   - Set the token to the environment variable:

   .. code-block:: bash

      export GITHUB_TOKEN=<your token>

That's it.

Github API client setup is done.

Search service
--------------

Now it's time to add ``SearchService``. It will:

- Perform the search.
- Fetch commit extra data for each result.
- Format result data.

``SearchService`` will use ``Github`` API client.

Create empty file ``services.py`` in the ``githubnavigator`` package:

.. code-block:: bash
   :emphasize-lines: 9

   ./
   ├── githubnavigator/
   │   ├── templates/
   │   │   ├── base.html
   │   │   └── index.html
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── services.py
   │   └── views.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Services module."""

   from github import Github
   from github.Repository import Repository
   from github.Commit import Commit


   class SearchService:
       """Search service performs search on Github."""

       def __init__(self, github_client: Github):
           self._github_client = github_client

       def search_repositories(self, query, limit):
           """Search for repositories and return formatted data."""
           repositories = self._github_client.search_repositories(
               query=query,
               **{"in": "name"},
           )
           return [
               self._format_repo(repository)
               for repository in repositories[:limit]
           ]

       def _format_repo(self, repository: Repository):
           commits = repository.get_commits()
           return {
               "url": repository.html_url,
               "name": repository.name,
               "owner": {
                   "login": repository.owner.login,
                   "url": repository.owner.html_url,
                   "avatar_url": repository.owner.avatar_url,
               },
               "latest_commit": self._format_commit(commits[0]) if commits else {},
           }

       def _format_commit(self, commit: Commit):
           return {
               "sha": commit.sha,
               "url": commit.html_url,
               "message": commit.commit.message,
               "author_name": commit.commit.author.name,
           }

Now let's add ``SearchService`` to the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 6,19-22

   """Containers module."""

   from dependency_injector import containers, providers
   from github import Github

   from . import services


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       github_client = providers.Factory(
           Github,
           login_or_token=config.github.auth_token,
           timeout=config.github.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           github_client=github_client,
       )

Inject search service into view
-------------------------------

Now we are ready to make the search work.

Let's inject ``SearchService`` into the ``index`` view. We will use :ref:`Wiring` feature.

Edit ``views.py``:

.. code-block:: python
   :emphasize-lines: 4,6-7,10-11,15

   """Views module."""

   from flask import request, render_template
   from dependency_injector.wiring import inject, Provide

   from .services import SearchService
   from .containers import Container


   @inject
   def index(search_service: SearchService = Provide[Container.search_service]):
       query = request.args.get("query", "Dependency Injector")
       limit = request.args.get("limit", 10, int)

       repositories = search_service.search_repositories(query, limit)

       return render_template(
           "index.html",
           query=query,
           limit=limit,
           repositories=repositories,
       )

To make the injection work we need to wire the container with the ``views`` module.
Let's configure the container to automatically make wiring with the ``views`` module when we
create a container instance.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 11

   """Containers module."""

   from dependency_injector import containers, providers
   from github import Github

   from . import services


   class Container(containers.DeclarativeContainer):

       wiring_config = containers.WiringConfiguration(modules=[".views"])

       config = providers.Configuration(yaml_files=["config.yml"])

       github_client = providers.Factory(
           Github,
           login_or_token=config.github.auth_token,
           timeout=config.github.request_timeout,
       )

       search_service = providers.Factory(
           services.SearchService,
           github_client=github_client,
       )

Make sure the app is running or use ``flask run`` and open ``http://127.0.0.1:5000/``.

You should see:

.. image::  flask-images/screen-02.png

Make some refactoring
---------------------

Our ``index`` view has two hardcoded config values:

- Default search query
- Default results limit

Let's make some refactoring. We will move these values to the config.

Edit ``views.py``:

.. code-block:: python
   :emphasize-lines: 11-17

   """Views module."""

   from flask import request, render_template
   from dependency_injector.wiring import inject, Provide

   from .services import SearchService
   from .containers import Container


   @inject
   def index(
           search_service: SearchService = Provide[Container.search_service],
           default_query: str = Provide[Container.config.default.query],
           default_limit: int = Provide[Container.config.default.limit.as_int()],
   ):
       query = request.args.get("query", default_query)
       limit = request.args.get("limit", default_limit, int)

       repositories = search_service.search_repositories(query, limit)

       return render_template(
           "index.html",
           query=query,
           limit=limit,
           repositories=repositories,
       )

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 3-5

   github:
     request_timeout: 10
   default:
     query: "Dependency Injector"
     limit: 10

That's it. The refactoring is done. We've made it cleaner.

Tests
-----

In this section we will add some tests.

We will use `pytest <https://docs.pytest.org/en/stable/>`_ with its Flask extension and
`coverage <https://coverage.readthedocs.io/>`_.

Edit ``requirements.txt``:

.. code-block:: bash
   :emphasize-lines: 6-7

   dependency-injector
   flask
   bootstrap-flask
   pygithub
   pyyaml
   pytest-flask
   pytest-cov

And install added packages:

.. code-block:: bash

   pip install -r requirements.txt

Create empty file ``tests.py`` in the ``githubnavigator`` package:

.. code-block:: bash
   :emphasize-lines: 10

   ./
   ├── githubnavigator/
   │   ├── templates/
   │   │   ├── base.html
   │   │   └── index.html
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── services.py
   │   ├── tests.py
   │   └── views.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python
   :emphasize-lines: 44,67

   """Tests module."""

   from unittest import mock

   import pytest
   from github import Github
   from flask import url_for

   from .application import create_app


   @pytest.fixture
   def app():
       app = create_app()
       yield app
       app.container.unwire()


   def test_index(client, app):
       github_client_mock = mock.Mock(spec=Github)
       github_client_mock.search_repositories.return_value = [
           mock.Mock(
               html_url="repo1-url",
               name="repo1-name",
               owner=mock.Mock(
                   login="owner1-login",
                   html_url="owner1-url",
                   avatar_url="owner1-avatar-url",
               ),
               get_commits=mock.Mock(return_value=[mock.Mock()]),
           ),
           mock.Mock(
               html_url="repo2-url",
               name="repo2-name",
               owner=mock.Mock(
                   login="owner2-login",
                   html_url="owner2-url",
                   avatar_url="owner2-avatar-url",
               ),
               get_commits=mock.Mock(return_value=[mock.Mock()]),
           ),
       ]

       with app.container.github_client.override(github_client_mock):
           response = client.get(url_for("index"))

       assert response.status_code == 200
       assert b"Results found: 2" in response.data

       assert b"repo1-url" in response.data
       assert b"repo1-name" in response.data
       assert b"owner1-login" in response.data
       assert b"owner1-url" in response.data
       assert b"owner1-avatar-url" in response.data

       assert b"repo2-url" in response.data
       assert b"repo2-name" in response.data
       assert b"owner2-login" in response.data
       assert b"owner2-url" in response.data
       assert b"owner2-avatar-url" in response.data


   def test_index_no_results(client, app):
       github_client_mock = mock.Mock(spec=Github)
       github_client_mock.search_repositories.return_value = []

       with app.container.github_client.override(github_client_mock):
           response = client.get(url_for("index"))

       assert response.status_code == 200
       assert b"Results found: 0" in response.data

Now let's run it and check the coverage:

.. code-block:: bash

   py.test githubnavigator/tests.py --cov=githubnavigator

You should see:

.. code-block:: bash

   platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
   plugins: cov-3.0.0, flask-1.2.0
   collected 2 items

   githubnavigator/tests.py ..                                     [100%]

   ---------- coverage: platform darwin, python 3.10.0-final-0 ----------
   Name                             Stmts   Miss  Cover
   ----------------------------------------------------
   githubnavigator/__init__.py          0      0   100%
   githubnavigator/application.py      13      0   100%
   githubnavigator/containers.py        8      0   100%
   githubnavigator/services.py         14      0   100%
   githubnavigator/tests.py            34      0   100%
   githubnavigator/views.py            10      0   100%
   ----------------------------------------------------
   TOTAL                               79      0   100%

.. note::

   Take a look at the highlights in the ``tests.py``.

   It emphasizes the overriding of the ``Github`` API client.

Conclusion
----------

In this tutorial we've built a ``Flask`` application following the dependency injection principle.
We've used the ``Dependency Injector`` as a dependency injection framework.

:ref:`containers` and :ref:`providers` helped to specify how to assemble search service and
integrate it with a 3rd-party library.

:ref:`configuration-provider` helped to deal with reading YAML file and environment variable.

We used :ref:`wiring` feature to inject the dependencies into the ``index()`` view.
:ref:`provider-overriding` feature helped in testing.

We kept all the dependencies injected explicitly. This will help when you need to add or
change something in future.

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask>`_.

What's next?

- Look at the other :ref:`tutorials`
- Know more about the :ref:`providers`
- Go to the :ref:`contents`

.. include:: ../sponsor.rst

.. disqus::
