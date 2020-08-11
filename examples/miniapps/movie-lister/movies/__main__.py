"""Main module."""

from .containers import ApplicationContainer


def main():
    container = ApplicationContainer()
    container.config.from_yaml('config.yml')
    container.config.storage.type.from_env('MOVIE_STORAGE_TYPE')

    storage = container.storage()
    fixtures = container.fixtures()
    storage.load_all(fixtures)

    lister = container.lister()
    print(lister.movies_directed_by('Francis Lawrence'))
    print(lister.movies_directed_by('Patricia Riggen'))
    print(lister.movies_directed_by('JJ Abrams'))
    print(lister.movies_released_in(2015))


if __name__ == '__main__':
    main()
