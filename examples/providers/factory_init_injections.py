"""`Factory` providers init injections example."""

from dependency_injector import providers


class Photo:
    ...


class User:
    def __init__(self, uid: int, main_photo: Photo) -> None:
        self.uid = uid
        self.main_photo = main_photo


photo_factory = providers.Factory(Photo)
user_factory = providers.Factory(
    User,
    main_photo=photo_factory,
)


if __name__ == '__main__':
    user1 = user_factory(1)
    # Same as: # user1 = User(1, main_photo=Photo())

    user2 = user_factory(2)
    # Same as: # user2 = User(2, main_photo=Photo())

    # Context keyword arguments have a priority:
    another_photo = Photo()
    user3 = user_factory(
        uid=3,
        main_photo=another_photo,
    )
    # Same as: # user3 = User(uid=3, main_photo=another_photo)
