"""Run example application."""

import sys
import logging

from containers import Platform, Application


if __name__ == '__main__':
    # Configure platform:
    Platform.configuration.update({'database': {'dsn': ':memory:'},
                                   'aws': {'access_key_id': 'KEY',
                                           'secret_access_key': 'SECRET'},
                                   'auth': {'token_ttl': 3600}})
    Platform.logger().addHandler(logging.StreamHandler(sys.stdout))

    # Run application:
    Application.main(uid=sys.argv[1],
                     password=sys.argv[2],
                     photo=sys.argv[3])

    # Previous call is an equivalent of next operations:
    #
    # logger = logging.Logger(name='example')
    # database = sqlite3.connect(':memory:')
    # s3 = boto.s3.connection.S3Connection(aws_access_key_id='KEY',
    #                                      aws_secret_access_key='SECRET')
    #
    # example.main.main(
    #     uid=sys.argv[1],
    #     password=sys.argv[2],
    #     photo=sys.argv[3],
    #     users_service=example.services.UsersService(logger=logger,
    #                                                 db=database),
    #     auth_service=example.services.AuthService(logger=logger,
    #                                               db=database,
    #                                               token_ttl=3600),
    #     photos_service=example.services.PhotosService(logger=logger,
    #                                                   db=database,
    #                                                   s3=s3))
