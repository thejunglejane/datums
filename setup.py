from setuptools import setup

from datums import __version__


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'datums',
    packages = ['datums', 'datums.pipeline', 'datums.models'],
    version = __version__,
    scripts = ['bin/datums'],
    install_requires = [
        'alembic', 'sqlalchemy', 'sqlalchemy-utils', 'python-dateutil'],
    tests_require = ['mock'],
    description = 'A PostgreSQL pipeline for Reporter.',
    author = 'Jane Stewart Adams',
    author_email = 'jane@thejunglejane.com',
    license = 'MIT', 
    url = 'https://github.com/thejunglejane/datums',
    download_url = 'https://github.com/thejunglejane/datums/tarball/{v}'.format(
        v=__version__)
)