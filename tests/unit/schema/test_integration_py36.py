import sqlite3
import unittest

from dependency_injector import containers

# Runtime import
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../',
    )),
)
_SAMPLES_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../samples/',
    )),
)
import sys
sys.path.append(_SAMPLES_DIR)

from schemasample.services import UserService, AuthService, PhotoService


class TestSchemaSingleContainer(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_yaml_schema(f'{_SAMPLES_DIR}/schemasample/container-single.yml')
        container.config.from_dict({
            'database': {
                'dsn': ':memory:',
            },
            'aws': {
                'access_key_id': 'KEY',
                'secret_access_key': 'SECRET',
            },
            'auth': {
                'token_ttl': 3600,
            },
        })

        # User service
        user_service1 = container.user_service()
        user_service2 = container.user_service()
        self.assertIsInstance(user_service1, UserService)
        self.assertIsInstance(user_service2, UserService)
        self.assertIsNot(user_service1, user_service2)

        self.assertIsInstance(user_service1.db, sqlite3.Connection)
        self.assertIsInstance(user_service2.db, sqlite3.Connection)
        self.assertIs(user_service1.db, user_service2.db)

        # Auth service
        auth_service1 = container.auth_service()
        auth_service2 = container.auth_service()
        self.assertIsInstance(auth_service1, AuthService)
        self.assertIsInstance(auth_service2, AuthService)
        self.assertIsNot(auth_service1, auth_service2)

        self.assertIsInstance(auth_service1.db, sqlite3.Connection)
        self.assertIsInstance(auth_service2.db, sqlite3.Connection)
        self.assertIs(auth_service1.db, auth_service2.db)
        self.assertIs(auth_service1.db, container.database_client())
        self.assertIs(auth_service2.db, container.database_client())

        self.assertEqual(auth_service1.token_ttl, 3600)
        self.assertEqual(auth_service2.token_ttl, 3600)

        # Photo service
        photo_service1 = container.photo_service()
        photo_service2 = container.photo_service()
        self.assertIsInstance(photo_service1, PhotoService)
        self.assertIsInstance(photo_service2, PhotoService)
        self.assertIsNot(photo_service1, photo_service2)

        self.assertIsInstance(photo_service1.db, sqlite3.Connection)
        self.assertIsInstance(photo_service2.db, sqlite3.Connection)
        self.assertIs(photo_service1.db, photo_service2.db)
        self.assertIs(photo_service1.db, container.database_client())
        self.assertIs(photo_service2.db, container.database_client())

        self.assertIs(photo_service1.s3, photo_service2.s3)
        self.assertIs(photo_service1.s3, container.s3_client())
        self.assertIs(photo_service2.s3, container.s3_client())


class TestSchemaMultipleContainers(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_yaml_schema(f'{_SAMPLES_DIR}/schemasample/container-multiple.yml')
        container.core.config.from_dict({
            'database': {
                'dsn': ':memory:',
            },
            'aws': {
                'access_key_id': 'KEY',
                'secret_access_key': 'SECRET',
            },
            'auth': {
                'token_ttl': 3600,
            },
        })

        # User service
        user_service1 = container.services.user()
        user_service2 = container.services.user()
        self.assertIsInstance(user_service1, UserService)
        self.assertIsInstance(user_service2, UserService)
        self.assertIsNot(user_service1, user_service2)

        self.assertIsInstance(user_service1.db, sqlite3.Connection)
        self.assertIsInstance(user_service2.db, sqlite3.Connection)
        self.assertIs(user_service1.db, user_service2.db)

        # Auth service
        auth_service1 = container.services.auth()
        auth_service2 = container.services.auth()
        self.assertIsInstance(auth_service1, AuthService)
        self.assertIsInstance(auth_service2, AuthService)
        self.assertIsNot(auth_service1, auth_service2)

        self.assertIsInstance(auth_service1.db, sqlite3.Connection)
        self.assertIsInstance(auth_service2.db, sqlite3.Connection)
        self.assertIs(auth_service1.db, auth_service2.db)
        self.assertIs(auth_service1.db, container.gateways.database_client())
        self.assertIs(auth_service2.db, container.gateways.database_client())

        self.assertEqual(auth_service1.token_ttl, 3600)
        self.assertEqual(auth_service2.token_ttl, 3600)

        # Photo service
        photo_service1 = container.services.photo()
        photo_service2 = container.services.photo()
        self.assertIsInstance(photo_service1, PhotoService)
        self.assertIsInstance(photo_service2, PhotoService)
        self.assertIsNot(photo_service1, photo_service2)

        self.assertIsInstance(photo_service1.db, sqlite3.Connection)
        self.assertIsInstance(photo_service2.db, sqlite3.Connection)
        self.assertIs(photo_service1.db, photo_service2.db)
        self.assertIs(photo_service1.db, container.gateways.database_client())
        self.assertIs(photo_service2.db, container.gateways.database_client())

        self.assertIs(photo_service1.s3, photo_service2.s3)
        self.assertIs(photo_service1.s3, container.gateways.s3_client())
        self.assertIs(photo_service2.s3, container.gateways.s3_client())


class TestSchemaMultipleContainersReordered(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_yaml_schema(f'{_SAMPLES_DIR}/schemasample/container-multiple-reordered.yml')
        container.core.config.from_dict({
            'database': {
                'dsn': ':memory:',
            },
            'aws': {
                'access_key_id': 'KEY',
                'secret_access_key': 'SECRET',
            },
            'auth': {
                'token_ttl': 3600,
            },
        })

        # User service
        user_service1 = container.services.user()
        user_service2 = container.services.user()
        self.assertIsInstance(user_service1, UserService)
        self.assertIsInstance(user_service2, UserService)
        self.assertIsNot(user_service1, user_service2)

        self.assertIsInstance(user_service1.db, sqlite3.Connection)
        self.assertIsInstance(user_service2.db, sqlite3.Connection)
        self.assertIs(user_service1.db, user_service2.db)

        # Auth service
        auth_service1 = container.services.auth()
        auth_service2 = container.services.auth()
        self.assertIsInstance(auth_service1, AuthService)
        self.assertIsInstance(auth_service2, AuthService)
        self.assertIsNot(auth_service1, auth_service2)

        self.assertIsInstance(auth_service1.db, sqlite3.Connection)
        self.assertIsInstance(auth_service2.db, sqlite3.Connection)
        self.assertIs(auth_service1.db, auth_service2.db)
        self.assertIs(auth_service1.db, container.gateways.database_client())
        self.assertIs(auth_service2.db, container.gateways.database_client())

        self.assertEqual(auth_service1.token_ttl, 3600)
        self.assertEqual(auth_service2.token_ttl, 3600)

        # Photo service
        photo_service1 = container.services.photo()
        photo_service2 = container.services.photo()
        self.assertIsInstance(photo_service1, PhotoService)
        self.assertIsInstance(photo_service2, PhotoService)
        self.assertIsNot(photo_service1, photo_service2)

        self.assertIsInstance(photo_service1.db, sqlite3.Connection)
        self.assertIsInstance(photo_service2.db, sqlite3.Connection)
        self.assertIs(photo_service1.db, photo_service2.db)
        self.assertIs(photo_service1.db, container.gateways.database_client())
        self.assertIs(photo_service2.db, container.gateways.database_client())

        self.assertIs(photo_service1.s3, photo_service2.s3)
        self.assertIs(photo_service1.s3, container.gateways.s3_client())
        self.assertIs(photo_service2.s3, container.gateways.s3_client())


class TestSchemaMultipleContainersWithInlineProviders(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_yaml_schema(f'{_SAMPLES_DIR}/schemasample/container-multiple-inline.yml')
        container.core.config.from_dict({
            'database': {
                'dsn': ':memory:',
            },
            'aws': {
                'access_key_id': 'KEY',
                'secret_access_key': 'SECRET',
            },
            'auth': {
                'token_ttl': 3600,
            },
        })

        # User service
        user_service1 = container.services.user()
        user_service2 = container.services.user()
        self.assertIsInstance(user_service1, UserService)
        self.assertIsInstance(user_service2, UserService)
        self.assertIsNot(user_service1, user_service2)

        self.assertIsInstance(user_service1.db, sqlite3.Connection)
        self.assertIsInstance(user_service2.db, sqlite3.Connection)
        self.assertIs(user_service1.db, user_service2.db)

        # Auth service
        auth_service1 = container.services.auth()
        auth_service2 = container.services.auth()
        self.assertIsInstance(auth_service1, AuthService)
        self.assertIsInstance(auth_service2, AuthService)
        self.assertIsNot(auth_service1, auth_service2)

        self.assertIsInstance(auth_service1.db, sqlite3.Connection)
        self.assertIsInstance(auth_service2.db, sqlite3.Connection)
        self.assertIs(auth_service1.db, auth_service2.db)
        self.assertIs(auth_service1.db, container.gateways.database_client())
        self.assertIs(auth_service2.db, container.gateways.database_client())

        self.assertEqual(auth_service1.token_ttl, 3600)
        self.assertEqual(auth_service2.token_ttl, 3600)

        # Photo service
        photo_service1 = container.services.photo()
        photo_service2 = container.services.photo()
        self.assertIsInstance(photo_service1, PhotoService)
        self.assertIsInstance(photo_service2, PhotoService)
        self.assertIsNot(photo_service1, photo_service2)

        self.assertIsInstance(photo_service1.db, sqlite3.Connection)
        self.assertIsInstance(photo_service2.db, sqlite3.Connection)
        self.assertIs(photo_service1.db, photo_service2.db)
        self.assertIs(photo_service1.db, container.gateways.database_client())
        self.assertIs(photo_service2.db, container.gateways.database_client())

        self.assertIs(photo_service1.s3, photo_service2.s3)
        self.assertIs(photo_service1.s3, container.gateways.s3_client())
        self.assertIs(photo_service2.s3, container.gateways.s3_client())


class TestSchemaBoto3Session(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_yaml_schema(f'{_SAMPLES_DIR}/schemasample/container-boto3-session.yml')
        container.config.from_dict(
            {
                'aws_access_key_id': 'key',
                'aws_secret_access_key': 'secret',
                'aws_session_token': 'token',
                'aws_region_name': 'us-east-1',
            },
        )

        self.assertEqual(container.s3_client().__class__.__name__, 'S3')
        self.assertEqual(container.sqs_client().__class__.__name__, 'SQS')
