#!/usr/bin/env python3

import argparse
from collections import Counter
import subprocess
import sys

import typing  # NOQA
from typing import List

if sys.version_info < (3, 0): # NOQA pragma: no cover
    raise SystemError("Must be using Python 3")

__version__ = '0.3.1'
STRIP_DOMAIN_USERNAMES = ['uber.com']
REVIEWERS_LIMIT = 7


class FindReviewers():
    def get_reviewers(self):  # type: () -> typing.Counter[str]
        """
        All review classes should implement this and return a list of strings
        representing reviewers
        """
        raise NotImplementedError()

    def run_command(self, command: List[str]) -> List[str]:
        """ Wrapper for running external subprocesses """
        process = subprocess.run(command, stdout=subprocess.PIPE)
        data = process.stdout.decode("utf-8").strip()
        if data:
            return data.split('\n')
        return []

    def extract_username_from_email(self, email: str) -> str:
        """ Given an email, extract the username for that email """
        domain = email[email.find('@')+1:]
        if domain in STRIP_DOMAIN_USERNAMES:
            return email[:email.find('@')]
        return email


class FindFileLogReviewers(FindReviewers):
    def extract_username_from_shortlog(self, shortlog: str) -> str:
        """ Given a line from a git shortlog, extract the username """
        shortlog = shortlog.strip()
        email = shortlog[shortlog.rfind("<")+1:]
        email = email[:email.find(">")]
        username = self.extract_username_from_email(email)
        return username

    def get_log_reviewers_from_file(self, file_path: str) -> List[str]:
        """ Find the reviewers based on the git log for a file """
        git_shortlog_command = ['git', 'shortlog', '-sne', file_path]
        git_shortlog = self.run_command(git_shortlog_command)
        users = [
            self.extract_username_from_shortlog(shortlog)
            for shortlog
            in git_shortlog
        ]
        users = [username for username in users if username]
        return users

    def get_changed_files(self) -> List[str]:
        raise NotImplementedError()

    def get_reviewers(self):  # type: () -> typing.Counter[str]
        """ Find the reviewers based on the git log of the diffed files """
        changed_files = self.get_changed_files()
        reviewers = Counter()  # type: typing.Counter[str]
        for changed in changed_files:
            users = self.get_log_reviewers_from_file(changed)
            reviewers.update(users)
        return reviewers


class FindDiffLogReviewers(FindFileLogReviewers):
    def get_changed_files(self) -> List[str]:
        """ Find the non-committed changed files """
        git_diff_files_command = ['git', 'diff-files', '--name-only']
        git_diff_files = self.run_command(git_diff_files_command)
        return git_diff_files


class FindLogReviewers(FindFileLogReviewers):
    def get_changed_files(self) -> List[str]:
        """ Find the changed files between current status and master """
        git_diff_files_command = ['git', 'diff', 'master', '--name-only']
        git_diff_files = self.run_command(git_diff_files_command)
        return git_diff_files


class FindArcCommitReviewers(FindLogReviewers):
    """
    Get reviewers based on arc commit messages, which list which users
    have approved past diffs
    """
    def get_log_reviewers_from_file(self, file_path: str) -> List[str]:
        git_commit_messages_command = ['git', 'log', '--all', file_path]
        git_commit_messages = self.run_command(git_commit_messages_command)
        reviewers_identifier = 'Reviewed By: '
        reviewers = []  # type: List[str]
        for line in git_commit_messages:
            if reviewers_identifier not in line:
                continue
            line = line.replace(reviewers_identifier, '')
            line_reviewers = line.split(', ')
            line_reviewers = [r.strip() for r in line_reviewers]
            reviewers += line_reviewers
        return reviewers


def show_reviewers(reviewers):  # type: (typing.Counter[str]) -> None
    reviewer_list = [x[0] for x in reviewers.most_common(REVIEWERS_LIMIT)]
    print(", ".join(reviewer_list))


def main() -> None:
    description = "Suggest reviewers for your diff.\n"
    description += "https://github.com/albertyw/git-reviewers"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--path',
        default='',
        help='relative path to the current git repository'
    )
    parser.add_argument(
        '-v', '--version', action='version', version=__version__,
    )
    parser.parse_args()

    finders = [FindDiffLogReviewers, FindLogReviewers, FindArcCommitReviewers]
    reviewers = Counter()  # type: typing.Counter[str]
    for finder in finders:
        finder_reviewers = finder().get_reviewers()
        reviewers.update(finder_reviewers)
    show_reviewers(reviewers)


if __name__ == "__main__":
    main()
