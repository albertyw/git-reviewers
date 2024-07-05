git-reviewers
=============

[![PyPI](https://img.shields.io/pypi/v/git-reviewers.svg)](https://pypi.org/project/git-reviewers/)
[![Python Versions](https://img.shields.io/pypi/pyversions/git-reviewers.svg)](https://pypi.org/project/git-reviewers/)


[![Build Status](https://drone.albertyw.com/api/badges/albertyw/git-reviewers/status.svg)](https://drone.albertyw.com/albertyw/git-reviewers)
[![Maintainability](https://api.codeclimate.com/v1/badges/58c63ec99d395f0f8df6/maintainability)](https://codeclimate.com/github/albertyw/git-reviewers/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/58c63ec99d395f0f8df6/test_coverage)](https://codeclimate.com/github/albertyw/git-reviewers/test_coverage)

Intelligently find code reviewers.
See also, [git-browse](https://github.com/albertyw/git-browse).

Installation
------------

### Homebrew (preferred for MacOS)

If you use Homebrew, you can install git-reviewers through the
[homebrew-albertyw tap](https://github.com/albertyw/homebrew-albertyw):


```bash
brew install albertyw/albertyw/git-reviewers
```

### Manual

If you don't use Homebrew, first clone this repository to somewhere on your system
(perhaps in your [dotfiles](https://github.com/albertyw/dotfiles)
repository), then run `<REPOSITORY_LOCATION>/install.sh`.

After installation, you can modify any default flags for git-reviewers
in `~/.gitconfig`

Usage
-----

```
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
```

Finders
-------

`git-reviewers` is componsed of a set of strategies for generating lists of
reviewers, or Finders.  They return a weighted set of reviewers which is then
sorted and recommended to you.  They include:

- `FindLogReviewers` - Generate a list of reviewers based on committers to
  your committed (but not merged with master) files
- `FindHistoricalReviewers` - Generate reviewers based on the repository
  committers as a whole
- `FindArcCommitReviewers` - Generate reviewers based on arc commit messages
  for files which you have modified on your branch

Configuration
-------------

`git-reviewers` supports reading configuration from a configuration file
with the `--json` flag.  The configuration file accepts json with the
following fields (all fields optional):

```json
{
    "verbose": false,
    "copy": false,
    "ignore": ["a", "b", "c"],
    "base_branch": "master"
}
```

`git-reviewers` will also by default search for and load a json
configuration file at `~/.git/reviewers`.

Development
-----------

```bash
pip install -e .[test]
ruff check .
mypy .
coverage run -m unittest
coverage report -m
```

Publishing
----------

```bash
pip install twine
python -m build
twine upload dist/*
```

Need to also update [albertyw/homebrew-albertyw](https://github.com/albertyw/homebrew-albertyw).
