Services mini application example (single container)
====================================================

.. meta::
   :description: "Services miniapp" is an example mini application that 
                 consists from several services that have dependencies on 
                 some standard and 3rd-party libraries for logging, 
                 interaction with database and remote service via API. 
                 "Services miniapp" example demonstrates usage of 
                 Dependency Injector for creating several inversion of control /
                 dependency injection containers.

"Services" is an example mini application. It consists from several services that have
dependencies on database & AWS S3.

.. image:: images/services-miniapp.png
    :width: 100%
    :align: center

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

Application structure
---------------------

Application consists from ``example`` package, several configuration files and ``requirements.txt``.

.. code-block:: bash

   ./
   ├── example/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   └── services.py
   ├── config.ini
   ├── logging.ini
   └── requirements.txt

Container
---------

Listing of ``example/containers.py``:

.. literalinclude:: ../../examples/miniapps/services-single-container/example/containers.py
   :language: python

Listing of ``example/__main__.py``:

.. literalinclude:: ../../examples/miniapps/services-single-container/example/__main__.py
   :language: python

Services
--------

Listing of ``example/services.py``:

.. literalinclude:: ../../examples/miniapps/services-single-container/example/services.py
   :language: python

Configuration
-------------

Listing of ``config.ini``:

.. literalinclude:: ../../examples/miniapps/services-single-container/config.ini
   :language: ini

Listing of ``logging.ini``:

.. literalinclude:: ../../examples/miniapps/services-single-container/logging.ini
   :language: ini

Sources on Github
-----------------

To find the source code navigate to the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/services-single-container>`_.

.. disqus::
