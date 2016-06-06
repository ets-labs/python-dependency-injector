"""Specializing dynamic container and factory provider example."""

import collections

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import dependency_injector.errors as errors


class SequenceProvider(providers.Factory):
    """Sequence factory.

    Can provide only sequence objects.
    """

    provided_type = collections.Sequence


sequences_container = containers.DynamicContainer()
sequences_container.provider_type = SequenceProvider


if __name__ == '__main__':
    try:
        sequences_container.object_provider = providers.Factory(object)
    except errors.Error as exception:
        print exception
        # <dependency_injector.containers.DynamicContainer object at
        # 0x107820ed0> can contain only <class '__main__.SequenceProvider'>
        # instances

    try:
        sequences_container.object_provider = SequenceProvider(object)
    except errors.Error as exception:
        print exception
        # <class '__main__.SequenceProvider'> can provide only
        # <class '_abcoll.Sequence'> instances

    sequences_container.list_provider = SequenceProvider(list)

    assert sequences_container.list_provider() == list()
