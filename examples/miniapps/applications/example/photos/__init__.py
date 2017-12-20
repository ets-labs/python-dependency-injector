"""Photos package."""

from core import containers
from core import providers

from . import entities
from . import repositories


class Photos(containers.DeclarativeContainer):
    """Photos package container."""

    database = providers.Dependency()
    file_storage = providers.Dependency()

    photo = providers.Factory(entities.Photo)
    photo_repository = providers.Singleton(repositories.PhotoRepository,
                                           object_factory=photo.provider,
                                           fs=file_storage,
                                           db=database)
