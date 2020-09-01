"""`Object` provider example."""

from dependency_injector import providers


object_provider = providers.Object(1)


if __name__ == '__main__':
    assert object_provider() == 1
