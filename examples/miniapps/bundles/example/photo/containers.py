"""Photo containers module."""

from dependency_injector import containers, providers

from . import entities, repositories


class PhotoContainer(containers.DeclarativeContainer):

    database = providers.Dependency()
    file_storage = providers.Dependency()

    photo = providers.Factory(entities.Photo)

    photo_repository = providers.Singleton(
        repositories.PhotoRepository,
        entity_factory=photo.provider,
        fs=file_storage,
        db=database,
    )
