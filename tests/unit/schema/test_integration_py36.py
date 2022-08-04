"""Container tests for building containers from configuration files."""

import os
import sqlite3

from dependency_injector import containers

from samples.schema.services import UserService, AuthService, PhotoService


SAMPLES_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        "../samples/",
    )),
)


def test_single_container_schema(container: containers.DynamicContainer):
    container.from_yaml_schema(f"{SAMPLES_DIR}/schema/container-single.yml")
    container.config.from_dict(
        {
            "database": {
                "dsn": ":memory:",
            },
            "aws": {
                "access_key_id": "KEY",
                "secret_access_key": "SECRET",
            },
            "auth": {
                "token_ttl": 3600,
            },
        },
    )

    # User service
    user_service1 = container.user_service()
    user_service2 = container.user_service()
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)
    assert user_service1 is not user_service2

    assert isinstance(user_service1.db, sqlite3.Connection)
    assert isinstance(user_service2.db, sqlite3.Connection)
    assert user_service1.db is user_service2.db

    # Auth service
    auth_service1 = container.auth_service()
    auth_service2 = container.auth_service()
    assert isinstance(auth_service1, AuthService)
    assert isinstance(auth_service2, AuthService)
    assert auth_service1 is not auth_service2

    assert isinstance(auth_service1.db, sqlite3.Connection)
    assert isinstance(auth_service2.db, sqlite3.Connection)
    assert auth_service1.db is auth_service2.db
    assert auth_service1.db is container.database_client()
    assert auth_service2.db is container.database_client()

    assert auth_service1.token_ttl == 3600
    assert auth_service2.token_ttl == 3600

    # Photo service
    photo_service1 = container.photo_service()
    photo_service2 = container.photo_service()
    assert isinstance(photo_service1, PhotoService)
    assert isinstance(photo_service2, PhotoService)
    assert photo_service1 is not photo_service2

    assert isinstance(photo_service1.db, sqlite3.Connection)
    assert isinstance(photo_service2.db, sqlite3.Connection)
    assert photo_service1.db is photo_service2.db
    assert photo_service1.db is container.database_client()
    assert photo_service2.db is container.database_client()

    assert photo_service1.s3 is photo_service2.s3
    assert photo_service1.s3 is container.s3_client()
    assert photo_service2.s3 is container.s3_client()


def test_multiple_containers_schema(container: containers.DynamicContainer):
    container.from_yaml_schema(f"{SAMPLES_DIR}/schema/container-multiple.yml")
    container.core.config.from_dict(
        {
            "database": {
                "dsn": ":memory:",
            },
            "aws": {
                "access_key_id": "KEY",
                "secret_access_key": "SECRET",
            },
            "auth": {
                "token_ttl": 3600,
            },
        },
    )

    # User service
    user_service1 = container.services.user()
    user_service2 = container.services.user()
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)
    assert user_service1 is not user_service2

    assert isinstance(user_service1.db, sqlite3.Connection)
    assert isinstance(user_service2.db, sqlite3.Connection)
    assert user_service1.db is user_service2.db

    # Auth service
    auth_service1 = container.services.auth()
    auth_service2 = container.services.auth()
    assert isinstance(auth_service1, AuthService)
    assert isinstance(auth_service2, AuthService)
    assert auth_service1 is not auth_service2

    assert isinstance(auth_service1.db, sqlite3.Connection)
    assert isinstance(auth_service2.db, sqlite3.Connection)
    assert auth_service1.db is auth_service2.db
    assert auth_service1.db is container.gateways.database_client()
    assert auth_service2.db is container.gateways.database_client()

    assert auth_service1.token_ttl == 3600
    assert auth_service2.token_ttl == 3600

    # Photo service
    photo_service1 = container.services.photo()
    photo_service2 = container.services.photo()
    assert isinstance(photo_service1, PhotoService)
    assert isinstance(photo_service2, PhotoService)
    assert photo_service1 is not photo_service2

    assert isinstance(photo_service1.db, sqlite3.Connection)
    assert isinstance(photo_service2.db, sqlite3.Connection)
    assert photo_service1.db is photo_service2.db
    assert photo_service1.db is container.gateways.database_client()
    assert photo_service2.db is container.gateways.database_client()

    assert photo_service1.s3 is photo_service2.s3
    assert photo_service1.s3 is container.gateways.s3_client()
    assert photo_service2.s3 is container.gateways.s3_client()


def test_multiple_reordered_containers_schema(container: containers.DynamicContainer):
    container.from_yaml_schema(f"{SAMPLES_DIR}/schema/container-multiple-reordered.yml")
    container.core.config.from_dict(
        {
            "database": {
                "dsn": ":memory:",
            },
            "aws": {
                "access_key_id": "KEY",
                "secret_access_key": "SECRET",
            },
            "auth": {
                "token_ttl": 3600,
            },
        },
    )

    # User service
    user_service1 = container.services.user()
    user_service2 = container.services.user()
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)
    assert user_service1 is not user_service2

    assert isinstance(user_service1.db, sqlite3.Connection)
    assert isinstance(user_service2.db, sqlite3.Connection)
    assert user_service1.db is user_service2.db

    # Auth service
    auth_service1 = container.services.auth()
    auth_service2 = container.services.auth()
    assert isinstance(auth_service1, AuthService)
    assert isinstance(auth_service2, AuthService)
    assert auth_service1 is not auth_service2

    assert isinstance(auth_service1.db, sqlite3.Connection)
    assert isinstance(auth_service2.db, sqlite3.Connection)
    assert auth_service1.db is auth_service2.db
    assert auth_service1.db is container.gateways.database_client()
    assert auth_service2.db is container.gateways.database_client()

    assert auth_service1.token_ttl == 3600
    assert auth_service2.token_ttl == 3600

    # Photo service
    photo_service1 = container.services.photo()
    photo_service2 = container.services.photo()
    assert isinstance(photo_service1, PhotoService)
    assert isinstance(photo_service2, PhotoService)
    assert photo_service1 is not photo_service2

    assert isinstance(photo_service1.db, sqlite3.Connection)
    assert isinstance(photo_service2.db, sqlite3.Connection)
    assert photo_service1.db is photo_service2.db
    assert photo_service1.db is container.gateways.database_client()
    assert photo_service2.db is container.gateways.database_client()

    assert photo_service1.s3 is photo_service2.s3
    assert photo_service1.s3 is container.gateways.s3_client()
    assert photo_service2.s3 is container.gateways.s3_client()


def test_multiple_containers_with_inline_providers_schema(container: containers.DynamicContainer):
    container.from_yaml_schema(f"{SAMPLES_DIR}/schema/container-multiple-inline.yml")
    container.core.config.from_dict(
        {
            "database": {
                "dsn": ":memory:",
            },
            "aws": {
                "access_key_id": "KEY",
                "secret_access_key": "SECRET",
            },
            "auth": {
                "token_ttl": 3600,
            },
        },
    )

    # User service
    user_service1 = container.services.user()
    user_service2 = container.services.user()
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)
    assert user_service1 is not user_service2

    assert isinstance(user_service1.db, sqlite3.Connection)
    assert isinstance(user_service2.db, sqlite3.Connection)
    assert user_service1.db is user_service2.db

    # Auth service
    auth_service1 = container.services.auth()
    auth_service2 = container.services.auth()
    assert isinstance(auth_service1, AuthService)
    assert isinstance(auth_service2, AuthService)
    assert auth_service1 is not auth_service2

    assert isinstance(auth_service1.db, sqlite3.Connection)
    assert isinstance(auth_service2.db, sqlite3.Connection)
    assert auth_service1.db is auth_service2.db
    assert auth_service1.db is container.gateways.database_client()
    assert auth_service2.db is container.gateways.database_client()

    assert auth_service1.token_ttl == 3600
    assert auth_service2.token_ttl == 3600

    # Photo service
    photo_service1 = container.services.photo()
    photo_service2 = container.services.photo()
    assert isinstance(photo_service1, PhotoService)
    assert isinstance(photo_service2, PhotoService)
    assert photo_service1 is not photo_service2

    assert isinstance(photo_service1.db, sqlite3.Connection)
    assert isinstance(photo_service2.db, sqlite3.Connection)
    assert photo_service1.db is photo_service2.db
    assert photo_service1.db is container.gateways.database_client()
    assert photo_service2.db is container.gateways.database_client()

    assert photo_service1.s3 is photo_service2.s3
    assert photo_service1.s3 is container.gateways.s3_client()
    assert photo_service2.s3 is container.gateways.s3_client()


def test_schema_with_boto3_session(container: containers.DynamicContainer):
    container.from_yaml_schema(f"{SAMPLES_DIR}/schema/container-boto3-session.yml")
    container.config.from_dict(
        {
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
            "aws_session_token": "token",
            "aws_region_name": "us-east-1",
        },
    )

    assert container.s3_client().__class__.__name__ == "S3"
    assert container.sqs_client().__class__.__name__ == "SQS"
