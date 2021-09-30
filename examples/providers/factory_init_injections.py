"""`Factory` provider init injections example."""

from dependency_injector import containers, providers


class Photo:
    ...


class User:
    def __init__(self, uid: int, main_photo: Photo) -> None:
        self.uid = uid
        self.main_photo = main_photo


class Container(containers.DeclarativeContainer):

    photo_factory = providers.Factory(Photo)

    user_factory = providers.Factory(
        User,
        main_photo=photo_factory,
    )


if __name__ == "__main__":
    container = Container()

    user1 = container.user_factory(1)
    # Same as: # user1 = User(1, main_photo=Photo())

    user2 = container.user_factory(2)
    # Same as: # user2 = User(2, main_photo=Photo())

    another_photo = Photo()
    user3 = container.user_factory(
        uid=3,
        main_photo=another_photo,
    )
    # Same as: # user3 = User(uid=3, main_photo=another_photo)
