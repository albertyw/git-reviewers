#!/usr/bin/env python3

import argparse
import subprocess
import sys

if sys.version_info < (3, 0):
    raise SystemError("Must be using Python 3")

UBER = True


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


def get_reviewers():
    reviewers = []
    git_shortlog_command = ['git', 'shortlog', '-sne']
    process = subprocess.run(git_shortlog_command, stdout=subprocess.PIPE)
    git_shortlog = process.stdout.decode("utf-8").split("\n")
    reviewers = [extract_username(shortlog) for shortlog in git_shortlog]
    reviewers = [username for username in reviewers if username]
    return reviewers


def show_reviewers(reviewers):
    print(", ".join(reviewers))


def main():
    description = "Suggest reviewers for your diff.\n"
    description += "https://github.com/albertyw/git-reviewers"
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()

    reviewers = get_reviewers()
    show_reviewers(reviewers)


if __name__ == "__main__":
    main()
