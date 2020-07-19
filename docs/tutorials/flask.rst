Flask tutorial
==============

This tutorials shows how to build ``Flask`` application following dependency injection principle.

What are we going to build?
---------------------------

We will build a web application that helps to search for repositories on Github. Let's call it
Github Navigator.

How does Github Navigator work?

- User opens a web page that asks to provide a search term.
- User types the search term and hits Enter.
- Github Navigator takes that and searches through the Github for matching repositories.
- When search is done Github Navigator returns user a web page with the result.
- The results page shows all matching repositories and the provided search term.
- For any matching repository user sees:
    - the repository name
    - the owner of the repository
    - the last commit to the repository
- User can click on the repository, the repository owner or the last commit to open its web page
  on the Github.

Prepare the environment
-----------------------

Let's create the environment for the project.

First we need to create a project folder and the virtual environment:

.. code-block:: bash

   mkdir ghnav-flask-tutorial
   cd ghnav-flask-tutorial
   python3 -m venv venv

Now let's activate the virtual environment:

.. code-block:: bash

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
   └requirements.txt

Now it's time to install ``Flask`` and ``Dependency Injector``.

Put next lines to the ``requirements.txt`` file::

   flask
   dependency-injector

Now let's install it::

   pip install -r requirements.txt

And check that installation is successful::

   python -c "import flask; print(flask.__version__)"
   python -c "import dependency_injector; print(dependency_injector.__version__)"


You should see something like::

   (venv) $ python -c "import flask; print(flask.__version__)"
   1.1.2
   (venv) $ python -c "import dependency_injector; print(dependency_injector.__version__)"
   3.22.0

*Versions can be different. That's fine.*

Hello world!
------------

Let's create minimal application.

Put next to the ``views.py``:

.. code-block:: python

    """Views module."""


    def index():
        return 'Hello, World!'

Ok, we have the view.

Now let's create the heart of our application - the container. Container will keep all of the
application components and their dependencies. First two providers we need to add are
the ``Flask`` application provider and the view provider.

Put next to the ``containers.py``:

.. code-block:: python

    """Application containers module."""

    from dependency_injector import containers
    from dependency_injector.ext import flask
    from flask import Flask

    from . import views


    class ApplicationContainer(containers.DeclarativeContainer):
        """Application container."""

        app = flask.Application(Flask, __name__)

        index_view = flask.View(views.index)

Finally we need to create the Flask application factory. It is traditionally called
``create_app()``. It will create the container. After that it will use the container to create
the Flask application. Last step is to configure the routing - we will assign ``index_view`` from the
container to handle user requests to the root ``/`` if our web application.

Put next to the ``application.py``:

.. code-block:: python

    """Application module."""

    from .containers import ApplicationContainer


    def create_app():
        """Create and return Flask application."""
        container = ApplicationContainer()

        app = container.app()
        app.container = container

        app.add_url_rule('/', view_func=container.index_view.as_view())

        return app

.. note::

   Container is the first object in the application.

   The container is used to create all other components.

Ok. Now we're ready to say "Hello, World!".

Do next in the terminal::

    export FLASK_APP=githubnavigator.application
    export FLASK_ENV=development
    flask run



The output should be something like::

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
