"""CLI Commands."""

import os
from setup import version
from manager import Manager


manager = Manager()


@manager.command
def publish(with_tag=True):
    """Publishg current version to PyPi."""
    os.system('python setup.py sdist upload')
    if with_tag:
        tag()


@manager.command
def tag():
    """Make tag from current version."""
    os.system('git tag -a {0} -m \'version {0}\''.format(version))
    os.system('git push --tags')


if __name__ == '__main__':
    manager.main()
