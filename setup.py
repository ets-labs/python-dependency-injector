"""
`Objects` setup script.
"""

import os
from setuptools import setup
from setuptools import Command


SHORT_DESCRIPTION = 'Dependency management tool for Python projects'


# Getting description.
with open('README.rst') as readme_file:
    description = readme_file.read()

    # Removing duplicated short description.
    description = description.replace(SHORT_DESCRIPTION, '')


# Getting requirements.
with open('requirements.txt') as version:
    requirements = version.readlines()


# Getting version.
with open('VERSION') as version:
    version = version.read().strip()


class PublishCommand(Command):

    """Setuptools `publish` command."""

    description = "Publish current distribution to PyPi and create tag"
    user_options = tuple()

    def initialize_options(self):
        """Init options."""

    def finalize_options(self):
        """Finalize options."""

    def run(self):
        """Command execution."""
        os.system('python setup.py sdist upload')
        os.system('git tag -a {0} -m \'version {0}\''.format(version))
        os.system('git push --tags')


setup(name='Objects',
      version=version,
      description=SHORT_DESCRIPTION,
      long_description=description,
      author='Roman Mogilatov',
      author_email='rmogilatov@gmail.com',
      maintainer='Roman Mogilatov',
      maintainer_email='rmogilatov@gmail.com',
      url='https://github.com/rmk135/objects',
      license='BSD New',
      packages=['objects'],
      zip_safe=True,
      install_requires=requirements,
      cmdclass={
          'publish': PublishCommand,
      },
      keywords=['Dependency management',
                'Dependency injection',
                'Dependency injection container',
                'DI',
                'DIC',
                'Dependency injector',
                'Inversion of Control',
                'Inversion of Control container',
                'IoC',
                'IoC container'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
