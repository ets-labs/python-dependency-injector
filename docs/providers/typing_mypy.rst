.. _provider-typing:

Typing and mypy
===============

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Providers,Typing,Mypy,
              Pattern,Example
   :description: Dependency Injector providers are mypy-friendly. Providers module goes with the
                 typing stubs to provide the typing information to ``mypy``, IDEs and editors.

Providers are ``mypy``-friendly.

Providers module goes with the typing stubs. It provides typing information to ``mypy`` and your
IDE.

.. code-block:: python

   from dependency_injector import providers


   class Animal:
       ...


   class Cat(Animal)
       ...


   provider = providers.Factory(Cat)


   if __name__ == "__main__":
       animal = provider()  # mypy knows that animal is of type "Cat"


You can use ``Provider`` as a generic type. This helps when a provider is an argument of a
function or method.

.. code-block:: python
   :emphasize-lines: 12

   from dependency_injector import providers


   class Animal:
       ...


   class Cat(Animal)
       ...


   provider: providers.Provider[Animal] = providers.Factory(Cat)


   if __name__ == "__main__":
       animal = provider()  # mypy knows that animal is of type "Animal"

.. disqus::
