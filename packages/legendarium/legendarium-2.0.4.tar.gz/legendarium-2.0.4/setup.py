#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='legendarium',
    version='2.0.4',
    description="Python library to handle SciELO's bibliographic legend",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jamil Atta Junior",
    author_email='jamil.atta@scielo.org',
    url='https://github.com/scieloorg/legendarium',
    packages=[
        'legendarium',
    ],
    package_dir={'legendarium':
                 'legendarium'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='legendarium',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
