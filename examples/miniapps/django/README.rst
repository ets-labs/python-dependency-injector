Django + Dependency Injector Example
====================================

This is a `Django <https://www.djangoproject.com/>`_ +
`Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application.

The example application helps to search for repositories on the Github.

.. image:: screenshot.png

Run
---

Create virtual environment:

.. code-block:: bash

   virtualenv venv
   . venv/bin/activate

Install requirements:

.. code-block:: bash

    pip install -r requirements.txt

Run migrations:

.. code-block:: bash

   python manage.py migrate

To run the application do:

.. code-block:: bash

   python manage.py runserver

The output should be something like:

.. code-block::

   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   October 05, 2020 - 03:17:05
   Django version 3.1.2, using settings 'githubnavigator.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.

After that visit http://127.0.0.1:8000/ in your browser.

.. note::

   Github has a rate limit. When the rate limit is exceed you will see an exception
   ``github.GithubException.RateLimitExceededException``. For unauthenticated requests, the rate
   limit allows for up to 60 requests per hour. To extend the limit to 5000 requests per hour you
   need to set personal access token.

   It's easy:

   - Follow this `guide <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_ to create a token.
   - Set a token to the environment variable:

   .. code-block:: bash

      export GITHUB_TOKEN=<your token>

   - Restart the app with ``python manage.py runserver``

   `Read more on Github rate limit <https://developer.github.com/v3/#rate-limiting>`_

Test
----

This application comes with the unit tests.

To run the tests do:

.. code-block:: bash

   coverage run --source='.' manage.py test && coverage report

The output should be something like:

.. code-block::

   Creating test database for alias 'default'...
   System check identified no issues (0 silenced).
   ..
   ----------------------------------------------------------------------
   Ran 2 tests in 0.037s

   OK
   Destroying test database for alias 'default'...
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   githubnavigator/__init__.py         4      0   100%
   githubnavigator/asgi.py             4      4     0%
   githubnavigator/containers.py       7      0   100%
   githubnavigator/services.py        14      0   100%
   githubnavigator/settings.py        23      0   100%
   githubnavigator/urls.py             3      0   100%
   githubnavigator/wsgi.py             4      4     0%
   manage.py                          12      2    83%
   web/__init__.py                     0      0   100%
   web/apps.py                         6      0   100%
   web/tests.py                       28      0   100%
   web/urls.py                         3      0   100%
   web/views.py                       12      0   100%
   ---------------------------------------------------
   TOTAL                             120     10    92%
