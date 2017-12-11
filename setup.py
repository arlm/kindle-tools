# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='kindle_tools',
    version='0.1.0',
    description='Python tools to extract data and hack your kindle device',
    long_description=readme,
    author='Alexandre Rocha Lima e Marcondes',
    author_email='alexandre.marcondes@gmail.com',
    url='https://github.com/arlm/kindle-tools',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)