#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read().splitlines()
test_requirements = open('tests/requirements.txt').read().splitlines()

setup(
    name='minreq',
    version='0.1.0',
    description="Check required data in a request.",
    long_description=readme + '\n\n' + history,
    author="Claudio Salazar",
    author_email='csalazar@spect.cl',
    url='https://github.com/csalazar/minreq',
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'minreq': 'minreq'},
    include_package_data=True,
    entry_points = {
        'console_scripts': ['minreq = minreq.cmdline:main']
    },
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='minreq',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
