Services mini application example (multiple containers)
=======================================================

.. meta::
   :description: "Services miniapp" is an example mini application that 
                 consists from several services that have dependencies on 
                 some standard and 3rd-party libraries for logging, 
                 interaction with database and remote service via API. 
                 "Services miniapp" example demonstrates usage of 
                 Dependency Injector for creating inversion of control /
                 dependency injection container.

"Services miniapp" is an example mini application that consists from several 
services that have dependencies on some standard and 3rd-party libraries for 
logging, interaction with database and remote service calls via API.

"Services miniapp" example demonstrates usage of 
:doc:`Dependency Injector <../index>` for creating IoC container.

Instructions for running:

.. code-block:: bash

    python run.py 1 secret photo.jpg

Example application
~~~~~~~~~~~~~~~~~~~

Classes diagram:

.. image:: /images/miniapps/services/classes.png
    :width: 100%
    :align: center


Example application structure:

.. code-block:: bash

    /example
        /__init__.py
        /main.py
        /services.py


Listing of ``example/services.py``:

.. literalinclude:: ../../examples/miniapps/services_v2/example/services.py
   :language: python

Listing of ``example/main.py``:

.. literalinclude:: ../../examples/miniapps/services_v2/example/main.py
   :language: python

IoC container
~~~~~~~~~~~~~

Listing of ``container.py``:

.. literalinclude:: ../../examples/miniapps/services_v2/container.py
   :language: python

Run application
~~~~~~~~~~~~~~~

Listing of ``run.py``:

.. literalinclude:: ../../examples/miniapps/services_v2/run.py
   :language: python


.. disqus::
