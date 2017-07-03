#!/bin/bash

# Installs this repository so that you can run `git reviewers` from anywhere in
# your filesystem

REPOSITORY_LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

git config --global \
    alias.reviewers \
    "!"$REPOSITORY_LOCATION"/git_reviewers/reviewers.py --path=\${GIT_PREFIX:-./}"
