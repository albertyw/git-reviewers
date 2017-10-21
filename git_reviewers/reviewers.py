#!/usr/bin/env python3

import argparse
import subprocess
import sys


if sys.version_info < (3, 0): # NOQA pragma: no cover
    raise SystemError("Must be using Python 3")

__version__ = '0.1.2'
UBER = False


class FindReviewers():
    def get_reviewers(self):
        raise NotImplementedError()

    def run_command(self, command):
        process = subprocess.run(command, stdout=subprocess.PIPE)
        data = process.stdout.decode("utf-8")
        return data

    def extract_username_from_email(self, email):
        if UBER:
            if email[-9:] == '@uber.com':
                return email[:-9]
            else:
                return None
        return email


class FindLogReviewers(FindReviewers):
    def extract_username_from_shortlog(self, shortlog):
        shortlog = shortlog.strip()
        email = shortlog[shortlog.rfind("<")+1:]
        email = email[:email.find(">")]
        username = self.extract_username_from_email(email)
        return username

    def get_changed_files(self):
        git_diff_files_command = ['git', 'diff-files']
        git_diff_files = self.run_command(git_diff_files_command)
        files = git_diff_files.split("\n")
        files = [x.split("\t")[-1].strip() for x in files]
        files = [x for x in files if x]
        return files

    def get_reviewers(self):
        changed_files = self.get_changed_files()
        reviewers = set()
        for changed in changed_files:
            git_shortlog_command = ['git', 'shortlog', '-sne', changed]
            git_shortlog = self.run_command(git_shortlog_command).split("\n")
            users = [
                self.extract_username_from_shortlog(shortlog)
                for shortlog
                in git_shortlog
            ]
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

    finder = FindLogReviewers()
    reviewers = finder.get_reviewers()
    show_reviewers(reviewers)


if __name__ == "__main__":
    main()
