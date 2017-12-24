#!/bin/bash

# Installs this repository so that you can run `git reviewers` from anywhere in
# your filesystem

# Check if python 3 is installed
if ! command -v python3 > /dev/null 2>&1; then
    echo "You must install python 3 to use git reviewers"
    echo "On OSX, use 'brew install python3'"
    echo "On Ubuntu/Debian, use 'sudo apt install python3'"
fi

if [ -z "$1" ]; then
  BROWSE_PY_LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  BROWSE_PY_LOCATION="$BROWSE_PY_LOCATION"/git_reviewers
else
  # Used for homebrew
  BROWSE_PY_LOCATION=$1
fi

git config --global \
    alias.reviewers \
    "!"$BROWSE_PY_LOCATION"/reviewers.py"
