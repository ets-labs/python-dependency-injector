"""Run example of dependency injection in Python."""

import sys
import logging

from container import IocContainer


if __name__ == '__main__':
    # Configure container:
    container = IocContainer(
        config={
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
        }
    )
    container.logger().addHandler(logging.StreamHandler(sys.stdout))

    # Run application:
    container.main(*sys.argv[1:])
