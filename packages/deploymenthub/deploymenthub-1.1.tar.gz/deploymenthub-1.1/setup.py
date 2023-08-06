import re
from io import open

from setuptools import find_packages, setup

PACKAGE_NAME = "deploymenthub"

setup(
    name=PACKAGE_NAME,
    version=1.01,
    description='A CLI client for deployment-hub server.',
    license='MIT',
    author='Jared Wines',
    author_email='contact@jaredwines.com',
    url='https://github.com/savoirfairelinux/num2words',
    packages=find_packages(exclude=['tests']),
    scripts=['bin/deploymenthub'],
)
