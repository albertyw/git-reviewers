# git-reviewers


[![PyPI](https://img.shields.io/pypi/v/git-reviewers.svg)](https://github.com/albertyw/git-reviewers)
[![PyPI](https://img.shields.io/pypi/pyversions/git-reviewers.svg)]()

[ ![Codeship Status for albertyw/git-reviewers](https://app.codeship.com/projects/17913cd0-3524-0135-2853-7e1f21584d06/status?branch=master)](https://app.codeship.com/projects/227040)
[![Dependency Status](https://gemnasium.com/badges/github.com/albertyw/git-reviewers.svg)](https://gemnasium.com/github.com/albertyw/git-reviewers)
[![Code Climate](https://codeclimate.com/github/albertyw/git-reviewers/badges/gpa.svg)](https://codeclimate.com/github/albertyw/git-reviewers)
[![Test Coverage](https://codeclimate.com/github/albertyw/git-reviewers/badges/coverage.svg)](https://codeclimate.com/github/albertyw/git-reviewers/coverage)

Tool to suggest code reviewers for your code depending on your diff

Installation
------------

You need to first clone this repository somewhere on your system (perhaps in
your [dotfiles](https://github.com/albertyw/dotfiles)) repository.

```bash
git clone git@github.com:albertyw/git-reviewers $REPOSITORY_LOCATION
git config --global \
    alias.reviewers \
        "!"$REPOSITORY_LOCATION"/git_reviewers/reviewers.py --path=\${GIT_PREFIX:-./}"
```

Usage
-----

```
Usage: git reviewers [-h] [--path PATH] [--uber]
```

If `--path` is called, then its value is be used to compute the relative path to the current git repository
If `--uber` is called, then the reviewers lookup and output will be compatible with Uber


Development
-----------

```bash
pip install -r requirements-test.txt
coverage run setup.py test
coverage report
flake8
```

Publishing
----------

```bash
sudo apt-get install pandoc
pip install twine pypandoc
python setup.py sdist bdist_wheel
twine upload dist/*
```
