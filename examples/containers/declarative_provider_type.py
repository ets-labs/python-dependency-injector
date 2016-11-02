"""Specializing declarative container and factory provider example."""

import collections

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import dependency_injector.errors as errors


class SequenceProvider(providers.Factory):
    """Sequence factory.

    Can provide only sequence objects.
    """

    provided_type = collections.Sequence


class SequencesContainer(containers.DeclarativeContainer):
    """IoC container.

    Can contain only sequence providers.
    """

    provider_type = SequenceProvider


if __name__ == '__main__':
    try:
        class _SequenceContainer1(SequencesContainer):
            object_provider = providers.Factory(object)
    except errors.Error as exception:
        print(exception)
        # <class '__main__._SequenceContainer1'> can contain only
        # <class '__main__.SequenceProvider'> instances

    try:
        class _SequenceContainer2(SequencesContainer):
            object_provider = SequenceProvider(object)
    except errors.Error as exception:
        print(exception)
        # <class '__main__.SequenceProvider'> can provide only
        # <class '_abcoll.Sequence'> instances

    class _SequenceContaier3(SequencesContainer):
        list_provider = SequenceProvider(list)

    assert _SequenceContaier3.list_provider() == list()
