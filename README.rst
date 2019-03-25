git-reviewers
=============

|PyPI| |Python Versions|

|Codeship Status for albertyw/git-reviewers| |Dependency Status| |Code
Climate| |Test Coverage|

Intelligently find code reviewers.
See also, git-browse_.

Installation
------------

Homebrew (preferred for MacOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use Homebrew, you can install git-reviewers through the
`homebrew-albertyw tap <https://github.com/albertyw/homebrew-albertyw>`__:

.. code:: bash

    brew install albertyw/albertyw/git-reviewers

Manual
~~~~~~

If you don't use Homebrew, first clone this repository to somewhere on your system
(perhaps in your dotfiles_
repository), then run ``<REPOSITORY_LOCATION>/install.sh``.

After installation, you can modify any default flags for git-reviewers
in ``~/.gitconfig``

Usage
-----

::

    usage: reviewers.py [-h] [-v] [--verbose] [-i IGNORE] [-j JSON] [-c]

    Suggest reviewers for your diff. https://github.com/albertyw/git-reviewers

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      --verbose             verbose mode
      -i IGNORE, --ignore IGNORE
                            ignore a list of reviewers (comma separated)
      -j JSON, --json JSON  json file to read configs from, overridden by CLI
                            flags
      -c, --copy            Copy the list of reviewers to clipboard, if available
      -b BASE_BRANCH, --base-branch BASE_BRANCH
                            Compare against a base branch (default: master)
Finders
-------

``git-reviewers`` is componsed of a set of strategies for generating lists of
reviewers, or Finders.  They return a weighted set of reviewers which is then
sorted and recommended to you.  They include:

 - ``FindLogReviewers`` - Generate a list of reviewers based on committers to
   your committed (but not merged with master) files
 - ``FindArcCommitReviewers`` - Generate reviewers based on arc commit messages
   for files which you have modified on your branch

Configuration
-------------

``git-reviewers`` supports reading configuration from a configuration file
with the ``--json`` flag.  The configuration file accepts json with the
following fields (all fields optional):

.. code:: json

    {
        "verbose": False,
        "copy": False,
        "ignore": ["a", "b", "c"],
        "branch": "master"
    }

``git-reviewers`` will also by default search for and load a json
configuration file at ``~/.git/reviewers``.

Development
-----------

.. code:: bash

    pip install -r requirements-test.txt
    coverage run setup.py test
    coverage report
    flake8

Publishing
----------

.. code:: bash

    pip install twine
    python setup.py sdist bdist_wheel
    twine upload dist/*

Need to also update `albertyw/homebrew-albertyw <https://github.com/albertyw/homebrew-albertyw>`_

.. _dotfiles: https://github.com/albertyw/dotfiles
.. _git-browse: https://github.com/albertyw/git-browse

.. |PyPI| image:: https://img.shields.io/pypi/v/git-reviewers.svg
   :target: https://github.com/albertyw/git-reviewers
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/git-reviewers.svg
   :target: https://github.com/albertyw/git-reviewers
.. |Codeship Status for albertyw/git-reviewers| image:: https://app.codeship.com/projects/17913cd0-3524-0135-2853-7e1f21584d06/status?branch=master
   :target: https://app.codeship.com/projects/227040
.. |Dependency Status| image:: https://pyup.io/repos/github/albertyw/git-reviewers/shield.svg
   :target: https://pyup.io/repos/github/albertyw/git-reviewers/
.. |Code Climate| image:: https://codeclimate.com/github/albertyw/git-reviewers/badges/gpa.svg
   :target: https://codeclimate.com/github/albertyw/git-reviewers
.. |Test Coverage| image:: https://codeclimate.com/github/albertyw/git-reviewers/badges/coverage.svg
   :target: https://codeclimate.com/github/albertyw/git-reviewers/coverage
