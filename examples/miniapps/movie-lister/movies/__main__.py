"""Main module."""

from .containers import ApplicationContainer


def main():
    container = ApplicationContainer()

    container.config.from_yaml('config.yml')
    container.config.finder.type.from_env('MOVIE_FINDER_TYPE')

    lister = container.lister()

    print(
        'Francis Lawrence movies:',
        lister.movies_directed_by('Francis Lawrence'),
    )
    print(
        '2016 movies:',
        lister.movies_released_in(2016),
    )


if __name__ == '__main__':
    main()
