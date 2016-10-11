"""Run example application."""

import sys
import logging

from containers import Platform, Application


if __name__ == '__main__':
    # Configure platform logger:
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
    # example.main.main(uid=sys.argv[1],
    #                   password=sys.argv[2],
    #                   photo=sys.argv[3],
    #                   users_service=example.services.Users(logger=logger,
    #                                                        db=database),
    #                   auth_service=example.services.Auth(logger=logger,
    #                                                      db=database,
    #                                                      token_ttl=3600),
    #                   photos_service=example.services.Photos(logger=logger,
    #                                                          db=database,
    #                                                          s3=s3))
