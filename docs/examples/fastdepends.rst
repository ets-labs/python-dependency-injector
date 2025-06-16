.. _fastdepends-example:

FastDepends example
===================

.. meta::
   :keywords: Python,Dependency Injection,FastDepends,Example
   :description: This example demonstrates a usage of the FastDepends and Dependency Injector.


This example demonstrates how to use ``Dependency Injector`` with `FastDepends <https://github.com/Lancetnik/FastDepends>`_, a lightweight dependency injection framework inspired by FastAPI's dependency system, but without the web framework components.

Basic Usage
-----------

The integration between FastDepends and Dependency Injector is straightforward. Simply use Dependency Injector's ``Provide`` marker within FastDepends' ``Depends`` function:

.. code-block:: python

    import sys

    from dependency_injector import containers, providers
    from dependency_injector.wiring import inject, Provide
    from fast_depends import Depends


    class CoefficientService:
        @staticmethod
        def get_coefficient() -> float:
            return 1.2


    class Container(containers.DeclarativeContainer):
        service = providers.Factory(CoefficientService)


    @inject
    def apply_coefficient(
        a: int,
        coefficient_provider: CoefficientService = Depends(Provide[Container.service]),
    ) -> float:
        return a * coefficient_provider.get_coefficient()


    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    apply_coefficient(100) == 120.0
