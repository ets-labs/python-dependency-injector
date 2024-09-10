.. _flask-example:

Flask example
=============

.. meta::
   :keywords: Python,Dependency Injection,Flask,Example
   :description: This example demonstrates a usage of the Flask and Dependency Injector.


This example shows how to use ``Dependency Injector`` with `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_.

The example application helps to search for repositories on the Github.

.. image:: images/flask.png
    :width: 100%
    :align: center

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask>`_.

:ref:`flask-tutorial` demonstrates how to build this application step-by-step.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── githubnavigator/
   │   ├── templates
   │   │   ├── base.html
   │   │   └── index.py
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── services.py
   │   ├── tests.py
   │   └── views.py
   ├── config.yml
   └── requirements.txt

Container
---------

Declarative container is defined in ``githubnavigator/containers.py``:

.. literalinclude:: ../../examples/miniapps/flask/githubnavigator/containers.py
   :language: python

Views
-----

View has dependencies on search service and some config options. The dependencies are injected
using :ref:`wiring` feature.

Listing of ``githubnavigator/views.py``:

.. literalinclude:: ../../examples/miniapps/flask/githubnavigator/views.py
   :language: python

Application factory
-------------------
Application factory creates container, wires it with the ``views`` module, creates
``Flask`` app and setup routes.

Listing of ``githubnavigator/application.py``:

.. literalinclude:: ../../examples/miniapps/flask/githubnavigator/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace github client with a mock ``githubnavigator/tests.py``:

.. literalinclude:: ../../examples/miniapps/flask/githubnavigator/tests.py
   :language: python
   :emphasize-lines: 44,67

Sources
-------

Explore the sources on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask>`_.

.. include:: ../sponsor.rst

.. disqus::
