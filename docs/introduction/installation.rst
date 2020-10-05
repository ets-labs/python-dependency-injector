Installation
============

``Dependency Injector`` is available on `PyPI <https://pypi.org/project/dependency-injector/>`_.
To install latest version you can use ``pip``:

.. code-block:: bash

    pip install dependency-injector

Some modules of the ``Dependency Injector`` are implemented as C extensions.
``Dependency Injector`` is distributed as a pre-compiled wheels. Wheels are
available for all supported Python versions on Linux, Windows and MacOS.
Linux distribution uses `manylinux <https://github.com/pypa/manylinux>`_.

If there is no appropriate wheel for your environment (Python version and OS)
installer will compile the package from sources on your machine. You'll need
a C compiler and Python header files.

To verify the installed version:

.. code-block:: bash

    >>> import dependency_injector
    >>> dependency_injector.__version__
    '4.0.0'

.. note::
    When add ``Dependency Injector`` to the ``requirements.txt`` don't forget to pin version
    to the current major:

    .. code-block:: bash

        dependency-injector>=4.0,<5.0

    *Next major version can be incompatible.*

All releases are available on `PyPI release history page <https://pypi.org/project/dependency-injector/#history>`_.
Each release has appropriate tag. The tags are available on
`GitHub releases page <https://github.com/ets-labs/python-dependency-injector/releases>`_.

.. disqus::
