from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Discovering Redis'

setup(
    name='rediscover',
    version=VERSION,
    author='Varun Chopra',
    author_email='pypi@varunchopra.vc',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['redis'],
)
