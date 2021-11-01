"""Main module."""

from dependency_injector.wiring import Provide, inject

from .user.repositories import UserRepository
from .photo.repositories import PhotoRepository
from .analytics.services import AggregationService
from .containers import ApplicationContainer


@inject
def main(
        user_repository: UserRepository = Provide[
            ApplicationContainer.user_package.user_repository
        ],
        photo_repository: PhotoRepository = Provide[
            ApplicationContainer.photo_package.photo_repository
        ],
        aggregation_service: AggregationService = Provide[
            ApplicationContainer.analytics_package.aggregation_service
        ],
) -> None:
    user1 = user_repository.get(id=1)
    user1_photos = photo_repository.get_photos(user1.id)
    print(f"Retrieve user id={user1.id}, photos count={len(user1_photos)}")

    user2 = user_repository.get(id=2)
    user2_photos = photo_repository.get_photos(user2.id)
    print(f"Retrieve user id={user2.id}, photos count={len(user2_photos)}")

    assert aggregation_service.user_repository is user_repository
    assert aggregation_service.photo_repository is photo_repository
    print("Aggregate analytics from user and photo packages")


if __name__ == "__main__":
    application = ApplicationContainer()
    application.wire(modules=[__name__])

    main()
