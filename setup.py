"""
`Objects` setup script.
"""

from setuptools import setup


# Getting description.
try:
    import pypandoc
except (IOError, ImportError):
    with open('README.md') as readme_file:
        description = readme_file.read()
else:
    description = pypandoc.convert('README.md', 'rst', format='markdown')


# Getting requirements.
with open('requirements.txt') as version:
    requirements = version.readlines()


# Getting version.
with open('VERSION') as version:
    version = version.read().strip()


setup(
    name='Objects',
    version=version,
    description='Python catalogs of objects providers',
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
    # keywords=['Dependency injection',
    #           'Dependency injection container',
    #           'DI',
    #           'DIC',
    #           'Dependency injector',
    #           'Inversion of Control',
    #           'Inversion of Control container',
    #           'IoC',
    #           'IoC container'],
    classifiers=[
        'Development Status :: 1 - Planning',
    #     'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.2',
    #     'Programming Language :: Python :: 3.3',
    #     'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    #     'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
