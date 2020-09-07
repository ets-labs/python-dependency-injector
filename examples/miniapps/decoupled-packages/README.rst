Decoupled packages example
==========================

Create virtual env:

.. code-block:: bash

   python3 -m venv venv
   . venv/bin/activate

Install requirements:

.. code-block:: bash

   pip install -r requirements.txt

Run:

.. code-block:: bash

   python -m example

You should see:

.. code-block:: bash

   Retrieve user id=1, photos count=5
   Retrieve user id=2, photos count=10
   Aggregate analytics from user and photo bundles
