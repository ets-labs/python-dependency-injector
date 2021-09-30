"""Tests module."""

from unittest import mock

import pytest
from fastapi.testclient import TestClient

from .repositories import UserRepository, UserNotFoundError
from .models import User
from .application import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_list(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.get_all.return_value = [
        User(id=1, email="test1@email.com", hashed_password="pwd", is_active=True),
        User(id=2, email="test2@email.com", hashed_password="pwd", is_active=False),
    ]

    with app.container.user_repository.override(repository_mock):
        response = client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"id": 1, "email": "test1@email.com", "hashed_password": "pwd", "is_active": True},
        {"id": 2, "email": "test2@email.com", "hashed_password": "pwd", "is_active": False},
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.get_by_id.return_value = User(
        id=1,
        email="xyz@email.com",
        hashed_password="pwd",
        is_active=True,
    )

    with app.container.user_repository.override(repository_mock):
        response = client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {"id": 1, "email": "xyz@email.com", "hashed_password": "pwd", "is_active": True}
    repository_mock.get_by_id.assert_called_once_with(1)


def test_get_by_id_404(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.get_by_id.side_effect = UserNotFoundError(1)

    with app.container.user_repository.override(repository_mock):
        response = client.get("/users/1")

    assert response.status_code == 404


@mock.patch("webapp.services.uuid4", return_value="xyz")
def test_add(_, client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.add.return_value = User(
        id=1,
        email="xyz@email.com",
        hashed_password="pwd",
        is_active=True,
    )

    with app.container.user_repository.override(repository_mock):
        response = client.post("/users")

    assert response.status_code == 201
    data = response.json()
    assert data == {"id": 1, "email": "xyz@email.com", "hashed_password": "pwd", "is_active": True}
    repository_mock.add.assert_called_once_with(email="xyz@email.com", password="pwd")


def test_remove(client):
    repository_mock = mock.Mock(spec=UserRepository)

    with app.container.user_repository.override(repository_mock):
        response = client.delete("/users/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


def test_remove_404(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.delete_by_id.side_effect = UserNotFoundError(1)

    with app.container.user_repository.override(repository_mock):
        response = client.delete("/users/1")

    assert response.status_code == 404


def test_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "OK"}
