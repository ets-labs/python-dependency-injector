"""Tests module."""

from unittest import mock

import pytest

from .containers import ApplicationContainer


@pytest.fixture
def container():
    container = ApplicationContainer()
    container.config.from_dict({
        'finder': {
            'type': 'csv',
            'csv': {
                'path': '/fake-movies.csv',
                'delimiter': ',',
            },
            'sqlite': {
                'path': '/fake-movies.db',
            },
        },
    })
    return container


def test_movies_directed_by(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie('The 33', 2015, 'Patricia Riggen'),
        container.movie('The Jungle Book', 2016, 'Jon Favreau'),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_directed_by('Jon Favreau')

    assert len(movies) == 1
    assert movies[0].name == 'The Jungle Book'


def test_movies_released_in(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie('The 33', 2015, 'Patricia Riggen'),
        container.movie('The Jungle Book', 2016, 'Jon Favreau'),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_released_in(2015)

    assert len(movies) == 1
    assert movies[0].name == 'The 33'
