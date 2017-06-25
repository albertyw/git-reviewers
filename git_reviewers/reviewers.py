#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

if sys.version_info < (3, 0): # NOQA pragma: no cover
    raise SystemError("Must be using Python 3")

UBER = False


def get_changed_files():
    git_diff_files_command = ['git', 'diff-files']
    process = subprocess.run(git_diff_files_command, stdout=subprocess.PIPE)
    git_diff_files = process.stdout.decode("utf-8")
    files = git_diff_files.split("\n")
    files = [x.split("\t")[-1].strip() for x in files]
    files = [x for x in files if x]
    return files


def extract_username(shortlog):
    shortlog = shortlog.strip()
    email = shortlog[shortlog.rfind("<")+1:]
    email = email[:email.find(">")]
    if UBER:
        if email[-9:] == '@uber.com':
            return email[:-9]
        else:
            return None
    return email


def get_reviewers(path, changed_files):
    path = os.path.join(os.getcwd(), path)
    reviewers = set()
    for changed in changed_files:
        git_shortlog_command = ['git', 'shortlog', '-sne', changed]
        process = subprocess.run(git_shortlog_command, stdout=subprocess.PIPE)
        git_shortlog = process.stdout.decode("utf-8").split("\n")
        users = [extract_username(shortlog) for shortlog in git_shortlog]
        users = [username for username in users if username]
        reviewers = reviewers.union(users)
    return reviewers


def show_reviewers(reviewers):
    print(", ".join(reviewers))


def main():
    global UBER
    description = "Suggest reviewers for your diff.\n"
    description += "https://github.com/albertyw/git-reviewers"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--path',
        default='',
        help='relative path to the current git repository'
    )
    parser.add_argument(
        '--uber',
        action="store_true",
        help='output reviewers list to work with uber repositories'
    )
    args = parser.parse_args()
    UBER = args.uber

    changed_files = get_changed_files()
    reviewers = get_reviewers(args.path, changed_files)
    show_reviewers(reviewers)


if __name__ == "__main__":
    main()
