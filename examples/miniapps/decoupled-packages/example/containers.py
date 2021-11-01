"""Containers module."""

import sqlite3

import boto3
from dependency_injector import containers, providers

from .user.containers import UserContainer
from .photo.containers import PhotoContainer
from .analytics.containers import AnalyticsContainer


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    sqlite = providers.Singleton(sqlite3.connect, config.database.dsn)

    s3 = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )

    user_package = providers.Container(
        UserContainer,
        database=sqlite,
    )

    photo_package = providers.Container(
        PhotoContainer,
        database=sqlite,
        file_storage=s3,
    )

    analytics_package = providers.Container(
        AnalyticsContainer,
        user_repository=user_package.user_repository,
        photo_repository=photo_package.photo_repository,
    )
