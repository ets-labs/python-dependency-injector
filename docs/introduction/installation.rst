Installation
============

*Dependency Injector* framework is distributed by PyPi_.

Latest stable version (and all previous versions) of *Dependency Injector* 
framework can be installed from PyPi_:

.. code-block:: bash

    pip install dependency-injector

.. note::
    Some components of *Dependency Injector* are implemented as C extension types. 
    *Dependency Injector* is distributed as an archive with a source code, so 
    C compiler and Python header files are required for the installation.

Sources can be cloned from GitHub_:

.. code-block:: bash

    git clone https://github.com/ets-labs/python-dependency-injector.git

Also all *Dependency Injector* releases can be downloaded from 
`GitHub releases page`_.

Verification of currently installed version could be done using 
:py:obj:`dependency_injector.VERSION` constant:

.. code-block:: bash

    >>> import dependency_injector
    >>> dependency_injector.__version__
    '3.43.0'

.. _PyPi: https://pypi.org/project/dependency-injector/
.. _GitHub: https://github.com/ets-labs/python-dependency-injector
.. _GitHub releases page: https://github.com/ets-labs/python-dependency-injector/releases


.. disqus::
