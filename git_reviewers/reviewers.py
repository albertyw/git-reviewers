#!/usr/bin/env python3

import argparse
from collections import Counter
import json
import os
import pathlib
import subprocess
import sys

import typing  # NOQA
from typing import List, Tuple

if sys.version_info < (3, 0): # NOQA pragma: no cover
    raise SystemError("Must be using Python 3")

__version__ = '0.12.0'
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

    def check_phabricator_activated(self, username: str) -> subprocess.Popen:
        """ Check whether a phabricator user has been activated by """
        phab_command = ['arc', 'call-conduit', 'user.search']
        request = '{"constraints": {"usernames": ["%s"]}}' % username
        process = subprocess.Popen(
            phab_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        process.stdin.write(request.encode("utf-8"))
        return process

    def parse_phabricator(self, username, process):
        # type: (str, subprocess.Popen) -> str
        stdout, stderr = process.communicate()
        output_str = stdout.decode("utf-8").strip()
        phab_output = json.loads(output_str)
        data = phab_output['response']['data']
        if not data:
            return username
        roles = data[0]['fields']['roles']
        if 'disabled' in roles:
            return ''
        return username

    def filter_phabricator_activated(self, usernames: List[str]) -> List[str]:
        username_processes = [
            (x, self.check_phabricator_activated(x)) for x in usernames
        ]
        usernames = [self.parse_phabricator(*x) for x in username_processes]
        usernames = [x for x in usernames if x]
        return usernames


class FindFileLogReviewers(FindReviewers):
    def extract_username_from_shortlog(self, shortlog: str) -> Tuple[str, int]:
        """ Given a line from a git shortlog, extract the username """
        shortlog = shortlog.strip()
        email = shortlog[shortlog.rfind("<")+1:]
        email = email[:email.find(">")]
        username = self.extract_username_from_email(email)
        count = int(shortlog.split("\t")[0])
        return username, count

    def get_log_reviewers_from_file(self, file_path):
        # type: (str) -> typing.Counter[str]
        """ Find the reviewers based on the git log for a file """
        git_shortlog_command = ['git', 'shortlog', '-sne', '--', file_path]
        git_shortlog = self.run_command(git_shortlog_command)
        users = dict(
            self.extract_username_from_shortlog(shortlog)
            for shortlog
            in git_shortlog
        )
        users = {
            reviewer: count for (reviewer, count)
            in users.items() if reviewer
        }
        return Counter(users)

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


class FindLogReviewers(FindFileLogReviewers):
    def get_changed_files(self) -> List[str]:
        """ Find the changed files between current status and master """
        git_diff_files_command = ['git', 'diff', 'master', '--name-only']
        git_diff_files = self.run_command(git_diff_files_command)
        if not git_diff_files:
            return FindHistoricalReviewers().get_changed_files()
        return git_diff_files


class FindHistoricalReviewers(FindFileLogReviewers):
    def get_changed_files(self) -> List[str]:
        """Find all git files """
        git_diff_files_command = [
            'git', 'ls-tree', '-r', 'master', '--name-only'
        ]
        git_diff_files = self.run_command(git_diff_files_command)
        return git_diff_files


class FindArcCommitReviewers(FindLogReviewers):
    """
    Get reviewers based on arc commit messages, which list which users
    have approved past diffs
    """
    def get_log_reviewers_from_file(self, file_path):
        # type: (str) -> typing.Counter[str]
        git_commit_messages_command = ['git', 'log', '--all', '--', file_path]
        git_commit_messages = self.run_command(git_commit_messages_command)
        reviewers_identifier = 'Reviewed By: '
        reviewers = Counter()  # type: typing.Counter[str]
        for line in git_commit_messages:
            if reviewers_identifier not in line:
                continue
            line = line.replace(reviewers_identifier, '')
            line_reviewers = line.split(', ')
            line_reviewers = [r.strip() for r in line_reviewers]
            reviewers.update(line_reviewers)
        return reviewers


def show_reviewers(reviewer_list, copy_clipboard):
    # type: (List[str], bool) -> None
    """ Output the reviewers to stdout and optionally to OS clipboard """
    reviewer_string = ", ".join(reviewer_list)
    print(reviewer_string)

    if not copy_clipboard:
        return
    try:
        p = subprocess.Popen(
            ['pbcopy', 'w'],
            stdin=subprocess.PIPE, close_fds=True
        )
        p.communicate(input=reviewer_string.encode('utf-8'))
    except FileNotFoundError:
        pass


def get_reviewers(ignores, verbose):  # type: (List[str], bool) -> List[str]
    """ Main function to get reviewers for a repository """
    phabricator = False
    finders = [FindLogReviewers, FindArcCommitReviewers]
    reviewers = Counter()  # type: typing.Counter[str]
    for finder in finders:
        finder_reviewers = finder().get_reviewers()
        if verbose:
            print(
                "Reviewers from %s: %s" %
                (finder.__name__, dict(finder_reviewers))
            )
        reviewers.update(finder_reviewers)
        if finder == FindArcCommitReviewers and finder_reviewers:
            phabricator = True

    most_common = [x[0] for x in reviewers.most_common()]
    most_common = [x for x in most_common if x not in ignores]
    if phabricator:
        most_common = FindArcCommitReviewers() \
                .filter_phabricator_activated(most_common)
    reviewers_list = most_common[:REVIEWERS_LIMIT]
    return reviewers_list


class Config():
    DEFAULT_GLOBAL_JSON = ".git/reviewers"
    VERBOSE_DEFAULT = None
    IGNORES_DEFAULT = ''
    JSON_DEFAULT = ''
    COPY_DEFAULT = None

    def __init__(self):
        self.verbose = False
        self.ignores = []
        self.json = ''
        self.copy = False

    @staticmethod
    def default_global_json():
        # type: () -> str
        """
        Return the path to the default config file for the current user
        """
        home_dir = str(pathlib.Path.home())
        json_path = os.path.join(home_dir, Config.DEFAULT_GLOBAL_JSON)
        return json_path

    def read_configs(self, args):
        # type: (argparse.Namespace) -> None
        """ Read config data """
        self.read_from_json(Config.default_global_json())
        self.read_from_json(args.json)
        self.read_from_args(args)

    def read_from_json(self, args_json):
        # type: (str) -> None
        """ Read configs from the json config file """
        self.json = args_json
        try:
            with open(self.json, 'r') as config_handle:
                config_data = config_handle.read()
            config = json.loads(config_data)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return
        if type(config) is not dict:
            return

        self.verbose = config.get('verbose', self.verbose)
        self.copy = config.get('copy', self.copy)
        self.ignores += config.get('ignore', self.ignores)

    def read_from_args(self, args):
        # type: (argparse.Namespace) -> None
        """ Parse configs by joining config file against argparse """
        if args.verbose != Config.VERBOSE_DEFAULT:
            self.verbose = args.verbose
        if args.copy != Config.VERBOSE_DEFAULT:
            self.copy = args.copy
        if args.ignore != Config.IGNORES_DEFAULT:
            self.ignores += args.ignore.split(',')


def main() -> None:
    """ Main entrypoint function to receive CLI arguments """
    description = "Suggest reviewers for your diff.\n"
    description += "https://github.com/albertyw/git-reviewers"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-v', '--version', action='version', version=__version__,
    )
    parser.add_argument(
        '--verbose',
        default=Config.VERBOSE_DEFAULT, action='store_true',
        help='verbose mode',
    )
    parser.add_argument(
        '-i', '--ignore',
        default=Config.IGNORES_DEFAULT,
        help='ignore a list of reviewers (comma separated)',
    )
    parser.add_argument(
        '-j', '--json',
        default=Config.JSON_DEFAULT,
        help='json file to read configs from, overridden by CLI flags',
    )
    parser.add_argument(
        '-c', '--copy',
        default=Config.COPY_DEFAULT, action='store_true',
        help='Copy the list of reviewers to clipboard, if available',
    )
    args = parser.parse_args()
    config = Config()
    config.read_configs(args)
    reviewers_list = get_reviewers(config.ignores, config.verbose)
    show_reviewers(reviewers_list, config.copy)


if __name__ == "__main__":
    main()
