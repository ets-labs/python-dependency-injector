"""CLI Commands."""

import os
from setup import version
from manager import Manager


manager = Manager()


@manager.command
def publish(with_tag=True):
    """Publish current version to PyPi."""
    os.system('python setup.py sdist upload')
    if with_tag:
        tag()


@manager.command
def tag():
    """Make tag from current version."""
    os.system('git tag -a {0} -m \'version {0}\''.format(version))
    os.system('git push --tags')


@manager.command
def check():
    """Check `objects` library and examples with code analyzers."""
    os.system('pylint objects/ --rcfile=./.pylintrc')
    os.system('flake8 objects/')
    os.system('pep257 objects/')

    os.system('flake8 examples/')
    os.system('pep257 examples/')


@manager.command
def test():
    """Run unittests."""
    os.system('find ./objects -name "*.pyc" -exec rm -rf {} \\;')
    os.system('find ./tests -name "*.pyc" -exec rm -rf {} \\;')

    os.system('find ./objects -name "*.pyo" -exec rm -rf {} \\;')
    os.system('find ./tests -name "*.pyo" -exec rm -rf {} \\;')

    os.system('coverage run --rcfile=./.coveragerc `which unit2` discover')
    os.system('coverage html --rcfile=./.coveragerc')
    os.system('rm -f .coverage')


if __name__ == '__main__':
    manager.main()
