"""Run example application."""

import containers


if __name__ == '__main__':
    containers.Application.main()

    # Previous call is an equivalent of next operations:
    #
    # database = sqlite3.connect(':memory:')
    # s3 = boto.s3.connection.S3Connection(aws_access_key_id='KEY',
    #                                      aws_secret_access_key='SECRET')
    #
    # example.main.main(users_service=example.services.Users(db=database),
    #                   auth_service=example.services.Auth(db=database,
    #                                                      token_ttl=3600),
    #                   photos_service=example.services.Photos(db=database,
    #                                                          s3=s3))
