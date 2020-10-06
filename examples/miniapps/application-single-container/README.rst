Application example (single container)
======================================

Create virtual env:

.. code-block:: bash

   python3 -m venv venv
   . venv/bin/activate

Install requirements:

.. code-block:: bash

   pip install -r requirements.txt

Run:

.. code-block:: bash

   python -m example user@example.com secret photo.jpg

You should see:

.. code-block:: bash

   [2020-10-06 15:32:33,195] [DEBUG] [example.services.UserService]: User user@example.com has been found in database
   [2020-10-06 15:32:33,195] [DEBUG] [example.services.AuthService]: User user@example.com has been successfully authenticated
   [2020-10-06 15:32:33,195] [DEBUG] [example.services.PhotoService]: Photo photo.jpg has been successfully uploaded by user user@example.com
