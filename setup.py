"""
`Objects` setup script.
"""

from setuptools import setup


DESCRIPTION = 'Dependency management tool for Python projects'


# Getting description.
with open('README.rst') as readme_file:
    description = readme_file.read()

    # Removing duplicated description
    description = description.replace(DESCRIPTION, '')


# Getting requirements.
with open('requirements.txt') as version:
    requirements = version.readlines()


# Getting version.
with open('VERSION') as version:
    version = version.read().strip()


if __name__ == '__main__':
    setup(
        name='Objects',
        version=version,
        description='Dependency management tool for Python projects',
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
        ]
    )
