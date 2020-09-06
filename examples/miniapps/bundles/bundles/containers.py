"""Containers module."""

import sqlite3

import boto3
from dependency_injector import containers, providers

from .user.containers import UserContainer
from .photo.containers import PhotoContainer
from .analytics.containers import AnalyticsContainer


class Application(containers.DeclarativeContainer):

    config = providers.Configuration()

    sqlite = providers.Singleton(sqlite3.connect, config.database.dsn)

    s3 = providers.Singleton(
        boto3.client,
        service_name='s3',
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )

    user_bundle = providers.Container(
        UserContainer,
        database=sqlite,
    )

    photo_bundle = providers.Container(
        PhotoContainer,
        database=sqlite,
        file_storage=s3,
    )

    analytics_bundle = providers.Container(
        AnalyticsContainer,
        user_repository=user_bundle.user_repository,
        photo_repository=photo_bundle.photo_repository,
    )
