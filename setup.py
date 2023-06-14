#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

from git_reviewers import reviewers

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Package meta-data.
NAME = 'git-reviewers'
DESCRIPTION = 'Suggest reviewers for your git branch'
URL = 'https://github.com/albertyw/git-reviewers'
EMAIL = 'git@albertyw.com'
AUTHOR = 'Albert Wang'


# Where the magic happens:
setup(
    name=NAME,
    version=reviewers.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,

    include_package_data=True,
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Version Control',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Typing :: Typed',
    ],

    keywords='git code review reviewer log history',

    # $ setup.py publish support.
    cmdclass={},

    package_data={"git_reviewers": ["py.typed"]},
    packages=find_packages(exclude=["tests"]),

    py_modules=["git_reviewers.reviewers"],

    python_requires='>=3.5',
    install_requires=[],

    test_suite="git_reviewers.tests",

    extras_require={
        'dev': [],
        'test': [],
    },


    data_files=[],

    entry_points={
        'console_scripts': [
            'git-reviewers=git_reviewers.reviewers:main',
        ],
    },
)
