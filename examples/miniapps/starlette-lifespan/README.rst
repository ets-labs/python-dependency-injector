Integration With Starlette-based Frameworks
===========================================

This is a `Starlette <https://www.starlette.io/>`_ +
`Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application
utilizing `lifespan API <https://www.starlette.io/lifespan/>`_ API to perform background jobs.

.. note::

    Pretty much `any framework built on top of Starlette <https://www.starlette.io/third-party-packages/#frameworks>`_
    supports this feature (`FastAPI <https://fastapi.tiangolo.com/advanced/events/#lifespan>`_,
    `Xpresso <https://xpresso-api.dev/latest/tutorial/lifespan/>`_, etc...).

.. note::

    It is discouraged to run long-lasting jobs in your web workers, you generally do not
    want to run business-related logic there. Use of background tasks in this example
    suits more of housekeeping tasks, like synchronizing feature flags, flushing caches or
    exporting internal metrics.

Run
---

Create virtual environment:

.. code-block:: bash

    python -m venv env
    . env/bin/activate

Install requirements:

.. code-block:: bash

    pip install -r requirements.txt

To run the application do:

.. code-block:: bash

    uvicorn --factory example:container.app
    # or
    python example.py

After that visit http://127.0.0.1:8000/ in your browser or use CLI command (``curl``, ``httpie``,
etc).
