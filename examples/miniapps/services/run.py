"""Run example application."""

import sys
import logging

from containers import Core, Application


if __name__ == '__main__':
    # Configure platform:
    Core.config.update({'database': {'dsn': ':memory:'},
                        'aws': {'access_key_id': 'KEY',
                                'secret_access_key': 'SECRET'},
                        'auth': {'token_ttl': 3600}})
    Core.logger().addHandler(logging.StreamHandler(sys.stdout))

    # Run application:
    Application.main(uid=sys.argv[1],
                     password=sys.argv[2],
                     photo=sys.argv[3])
