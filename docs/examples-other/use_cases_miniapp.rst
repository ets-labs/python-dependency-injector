Use cases mini application example
----------------------------------

.. currentmodule:: dependency_injector.providers

"Use cases" miniapp demonstrate usage of :py:class:`DependenciesContainer` 
provider.

Example application
~~~~~~~~~~~~~~~~~~~

"Use cases" mini application has next structure:

.. code-block:: bash

    use_cases/
        example/               <-- Example package
            __init__.py
            adapters.py
            use_cases.py
        containers.py          <-- Dependency injection containers
        run.py                 <-- Entrypoint


IoC containers
~~~~~~~~~~~~~~

Listing of ``use_cases/containers.py``:

.. literalinclude:: ../../examples/miniapps/use_cases/containers.py
   :language: python

Run application
~~~~~~~~~~~~~~~

Listing of ``run.py``:

.. literalinclude:: ../../examples/miniapps/use_cases/run.py
   :language: python

Instructions for running:

.. code-block:: bash

    python run.py prod example@example.com  # Running in "production" environment
    python run.py test example@example.com  # Running in "testing" environment

Links
~~~~~

+ `Dependency Injector <https://github.com/ets-labs/python-dependency-injector/>`_
+ `Full example sources <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/use_cases>`_


.. disqus::
