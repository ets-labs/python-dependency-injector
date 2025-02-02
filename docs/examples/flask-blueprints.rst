.. _flask-blueprints-example:

Flask blueprints example
========================

.. meta::
   :keywords: Python,Dependency Injection,Flask,Blueprints,Example
   :description: This example demonstrates a usage of the Flask Blueprints and Dependency Injector.


This example shows how to use ``Dependency Injector`` with `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_
blueprints.

The example application helps to search for repositories on the Github.

.. image:: images/flask.png
    :width: 100%
    :align: center

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask-blueprints>`_.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── githubnavigator/
   │   ├── blueprints
   │   │   ├── __init__.py
   │   │   └── example.py
   │   ├── templates
   │   │   ├── base.html
   │   │   └── index.py
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── services.py
   │   └── tests.py
   ├── config.yml
   └── requirements.txt

Container
---------

Declarative container is defined in ``githubnavigator/containers.py``:

.. literalinclude:: ../../examples/miniapps/flask-blueprints/githubnavigator/containers.py
   :language: python

Blueprints
----------

Blueprint's view has dependencies on search service and some config options. The dependencies are injected
using :ref:`wiring` feature.

Listing of ``githubnavigator/blueprints/example.py``:

.. literalinclude:: ../../examples/miniapps/flask-blueprints/githubnavigator/blueprints/example.py
   :language: python

Application factory
-------------------

Application factory creates container, wires it with the blueprints, creates
``Flask`` app, and setup routes.

Listing of ``githubnavigator/application.py``:

.. literalinclude:: ../../examples/miniapps/flask-blueprints/githubnavigator/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace github client with a mock ``githubnavigator/tests.py``:

.. literalinclude:: ../../examples/miniapps/flask-blueprints/githubnavigator/tests.py
   :language: python
   :emphasize-lines: 44,67

Sources
-------

Explore the sources on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/flask-blueprints>`_.

.. include:: ../sponsor.rst

.. disqus::
