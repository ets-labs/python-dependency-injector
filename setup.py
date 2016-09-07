"""`Dependency injector` setup script."""

import os
import re

from setuptools import setup
from setuptools import Command


# Getting description:
with open('README.rst') as readme_file:
    description = readme_file.read()

# Getting requirements:
with open('requirements.txt') as version:
    requirements = version.readlines()

# Getting version:
with open('dependency_injector/__init__.py') as init_file:
    version = re.search('VERSION = \'(.*?)\'', init_file.read()).group(1)


class PublishCommand(Command):
    """Setuptools `publish` command."""

    description = "Publish current distribution to PyPi and create tag"
    user_options = []

    def initialize_options(self):
        """Init options."""

    def finalize_options(self):
        """Finalize options."""

    def run(self):
        """Command execution."""
        self.run_command('sdist')
        self.run_command('upload')
        os.system('git tag -a {0} -m \'version {0}\''.format(version))
        os.system('git push --tags')


setup(name='dependency-injector',
      version=version,
      description='Python dependency injection framework',
      long_description=description,
      author='ETS Labs',
      author_email='rmogilatov@gmail.com',
      maintainer='Roman Mogilatov',
      maintainer_email='rmogilatov@gmail.com',
      url='https://github.com/ets-labs/python-dependency-injector',
      bugtrack_url='https://github.com/ets-labs/python-dependency-injector' +
                   '/issues',
      download_url='https://pypi.python.org/pypi/dependency_injector',
      license='BSD New',
      packages=['dependency_injector',
                'dependency_injector.providers'],
      platforms=['any'],
      zip_safe=True,
      install_requires=requirements,
      cmdclass={
          'publish': PublishCommand,
      },
      keywords=[
          'DI',
          'Dependency injection',
          'IoC',
          'Inversion of Control',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
