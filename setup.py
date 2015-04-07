from setuptools import setup

from datums import __version__


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'datums',
    packages = ['datums.pipeline', 'datums.models'],
    scripts = ['bin/datums'],
    version = __version__,
    description = 'A PostgreSQL pipeline for Reporter data.',
    author = 'Jane Stewart Adams',
    author_email = 'jane@thejunglejane.com',
    install_requires = ['sqlalchemy']
)