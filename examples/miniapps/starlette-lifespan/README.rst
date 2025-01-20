Integration With Starlette-based Frameworks
===========================================

This is a `Starlette <https://www.starlette.io/>`_ +
`Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_ example application
utilizing `lifespan API <https://www.starlette.io/lifespan/>`_.

.. note::

    Pretty much `any framework built on top of Starlette <https://www.starlette.io/third-party-packages/#frameworks>`_
    supports this feature (`FastAPI <https://fastapi.tiangolo.com/advanced/events/#lifespan>`_,
    `Xpresso <https://xpresso-api.dev/latest/tutorial/lifespan/>`_, etc...).

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

    python example.py
    # or (logging won't be configured):
    uvicorn --factory example:container.app

After that visit http://127.0.0.1:8000/ in your browser or use CLI command (``curl``, ``httpie``,
etc).
