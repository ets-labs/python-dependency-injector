Advanced usage
==============

Below you can find some variants of advanced usage of *Objects*.

@inject decorator
-----------------

``@inject`` decorator could be used for patching any callable with injection.
Any Python object will be injected *as is*, except *Objects* providers,
that will be called to provide injectable value.

.. code-block:: python

    """`@inject` decorator example."""

    from objects.providers import NewInstance

    from objects.injections import KwArg
    from objects.injections import inject


    new_object = NewInstance(object)


    @inject(KwArg('object_a', new_object))
    @inject(KwArg('some_setting', 1334))
    def example_callback(object_a, some_setting):
        """This function has dependencies on object a and b.

        Dependencies are injected using `@inject` decorator.
        """
        assert isinstance(object_a, object)
        assert some_setting == 1334


    example_callback()
    example_callback()
