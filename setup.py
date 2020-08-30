from setuptools import find_packages
from setuptools import setup

setup(
    name='awesome',
    version='0.1.0',
    license=' Apache License, Version 2.0',
    description='PySpark: unit, integration and end to end tests',
    author='Gustavo Martin Morcuende',

    url='https://gumartinm.name/',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
