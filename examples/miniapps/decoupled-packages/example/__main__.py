"""Main module."""

from .containers import ApplicationContainer


if __name__ == '__main__':
    application = ApplicationContainer()
    application.config.from_ini('config.ini')

    user_repository = application.user_package.user_repository()
    photo_repository = application.photo_package.photo_repository()

    user1 = user_repository.get(id=1)
    user1_photos = photo_repository.get_photos(user1.id)
    print(f'Retrieve user id={user1.id}, photos count={len(user1_photos)}')

    user2 = user_repository.get(id=2)
    user2_photos = photo_repository.get_photos(user2.id)
    print(f'Retrieve user id={user2.id}, photos count={len(user2_photos)}')

    aggregation_service = application.analytics_package.aggregation_service()
    assert aggregation_service.user_repository is user_repository
    assert aggregation_service.photo_repository is photo_repository
    print('Aggregate analytics from user and photo packages')
