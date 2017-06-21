# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from the README file
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    print("pypandoc not installed, not converting markdown to rst")
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='git-reviewers',

    version='0.0.2',

    description='Suggest reviewers for your git branch',
    long_description=long_description,

    url='https://github.com/albertyw/git-reviewers',

    author='Albert Wang',
    author_email='git@albertyw.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Version Control',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='git code review reviewer log history',

    packages=find_packages("git_reviewers", exclude=["tests"]),

    py_modules=["git_reviewers.reviewers"],

    install_requires=[],

    test_suite="git_reviewers.tests",

    # testing requires flake8 and coverage but they're listed separately
    # because they need to wrap setup.py
    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={},

    data_files=[],

    entry_points={
        'console_scripts': [
            'git_reviewers=git_reviewers.reviewers:main',
        ],
    },
)
