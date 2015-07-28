Inline injections
=================

@inject decorator
-----------------

``@inject`` decorator can be used for making *inline* dependency injections.
It *patches* decorated callable in such way that dependency injection will be
done before every call of decorated callable.

``@inject`` decorator takes only argument that is supposed to be an
``objects.injections.Injection`` instance.

Any Python object will be injected *as is*, except *Objects* providers,
that will be called to provide injectable value.

Below is an example of how Flask's view could be patched using ``@inject``
decorator:

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

