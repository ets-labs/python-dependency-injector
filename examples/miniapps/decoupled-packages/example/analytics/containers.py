"""Analytics containers module."""

from dependency_injector import containers, providers

from . import services


class AnalyticsContainer(containers.DeclarativeContainer):

    user_repository = providers.Dependency()
    photo_repository = providers.Dependency()

    aggregation_service = providers.Singleton(
        services.AggregationService,
        user_repository=user_repository,
        photo_repository=photo_repository,
    )
