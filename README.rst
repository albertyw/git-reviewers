git-reviewers
=============

|PyPI| |Python Versions|

|Codeship Status for albertyw/git-reviewers| |Dependency Status| |Code
Climate| |Test Coverage|

Tool to suggest code reviewers for your code depending on your diff

Installation
------------

First clone this repository to somewhere on your system
(perhaps in your `dotfiles <https://github.com/albertyw/dotfiles>`__
repository), then run ``<REPOSITORY_LOCATION>/install.sh``.

Usage
-----

::

    Usage: git reviewers [-h] [--path PATH]

If ``--path`` is called, then its value is be used to compute the
relative path to the current git repository.

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

.. _dotfiles: https://github.com/albertyw/dotfiles

.. |PyPI| image:: https://img.shields.io/pypi/v/git-reviewers.svg
   :target: https://github.com/albertyw/git-reviewers
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/git-reviewers.svg
   :target: https://github.com/albertyw/git-reviewers
.. |Codeship Status for albertyw/git-reviewers| image:: https://app.codeship.com/projects/17913cd0-3524-0135-2853-7e1f21584d06/status?branch=master
   :target: https://app.codeship.com/projects/227040
.. |Dependency Status| image:: https://gemnasium.com/badges/github.com/albertyw/git-reviewers.svg
   :target: https://gemnasium.com/githu%20b.com/albertyw/git-reviewers
.. |Code Climate| image:: https://codeclimate.com/github/albertyw/git-reviewers/badges/gpa.svg
   :target: https://codeclimate.com/github%20/albertyw/git-reviewers
.. |Test Coverage| image:: https://codeclimate.com/github/albertyw/git-reviewers/badges/coverage.svg
   :target: https://codeclimate.com/%20github/albertyw/git-reviewers/coverage
