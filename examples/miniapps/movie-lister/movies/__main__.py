"""Main module."""

from dependency_injector.wiring import Provide, inject

from .listers import MovieLister
from .containers import Container


@inject
def main(lister: MovieLister = Provide[Container.lister]) -> None:
    print("Francis Lawrence movies:")
    for movie in lister.movies_directed_by("Francis Lawrence"):
        print("\t-", movie)

    print("2016 movies:")
    for movie in lister.movies_released_in(2016):
        print("\t-", movie)


if __name__ == "__main__":
    container = Container()
    container.config.finder.type.from_env("MOVIE_FINDER_TYPE")
    container.wire(modules=[__name__])

    main()
