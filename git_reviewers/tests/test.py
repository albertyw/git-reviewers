from collections import Counter
import os
import json
import sys
import tempfile
import typing
import unittest
from unittest.mock import patch, MagicMock

from git_reviewers import reviewers
from git_reviewers.tests.fixtures import \
    PHAB_DEFAULT_DATA, \
    PHAB_ACTIVATED_DATA, \
    PHAB_DISABLED_DATA

directory = os.path.dirname(os.path.realpath(__file__))
BASE_DIRECTORY = os.path.normpath(os.path.join(directory, '..', '..'))


class TestFindReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindReviewers(reviewers.Config())
        self.orig_reviewers_limit = reviewers.REVIEWERS_LIMIT

    def tearDown(self):
        reviewers.REVIEWERS_LIMIT = self.orig_reviewers_limit

    def test_get_reviewers(self):
        with self.assertRaises(NotImplementedError):
            self.finder.get_reviewers()

    @patch('subprocess.run')
    def test_run_command(self, mock_run):
        mock_run().stdout = b'asdf'
        data = self.finder.run_command(['ls'])
        self.assertEqual(data, ['asdf'])

    @patch('subprocess.run')
    def test_run_command_empty_response(self, mock_run):
        mock_run().stdout = b''
        data = self.finder.run_command([':'])
        self.assertEqual(data, [])

    def check_extract_username(self, email, expected_user):
        user = self.finder.extract_username_from_email(email)
        self.assertEqual(user, expected_user)

    def test_extract_username_from_generic_email(self):
        self.check_extract_username('asdf@gmail.com', 'asdf@gmail.com')

    def test_extract_uber_username_from_email(self):
        self.check_extract_username('asdf@uber.com', 'asdf')

    @patch('subprocess.Popen')
    def test_check_phabricator_activated(self, mock_popen):
        mock_popen().communicate.return_value = [PHAB_ACTIVATED_DATA, '']
        activated = self.finder.check_phabricator_activated('asdf')
        self.assertTrue(activated)

    @patch('subprocess.Popen')
    def test_check_phabricator_activated_none(self, mock_popen):
        mock_popen().communicate.return_value = [PHAB_DEFAULT_DATA, '']
        activated = self.finder.check_phabricator_activated('asdf')
        self.assertTrue(activated)

    def test_filter_phabricator_activated(self):
        users = ['a', 'b', 'c', 'd']
        reviewers.REVIEWERS_LIMIT = 2
        self.mock_check_count = 0

        def mock_check(u):
            self.assertEqual(u, users[self.mock_check_count])
            self.mock_check_count += 1
            return self.mock_check_count - 1
        self.mock_parse_count = 0

        def mock_parse(u, p):
            self.assertEqual(u, users[self.mock_parse_count])
            self.assertEqual(p, self.mock_parse_count)
            parse_return = ''
            if self.mock_parse_count in [0, 2]:
                parse_return = u
            self.mock_parse_count += 1
            return parse_return
        self.finder.check_phabricator_activated = mock_check
        self.finder.parse_phabricator = mock_parse
        filtered_usernames = self.finder.filter_phabricator_activated(users)
        self.assertEqual(self.mock_check_count, 3)
        self.assertEqual(self.mock_parse_count, 3)
        self.assertEqual(filtered_usernames, ['a', 'c'])


class TestFindLogReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindFileLogReviewers(reviewers.Config())

    def check_extract_username_from_shortlog(self, shortlog, email, weight):
        user_data = self.finder.extract_username_from_shortlog(shortlog)
        self.assertEqual(user_data, (email, weight))

    def test_gets_generic_emails(self):
        shortlog = '     3\tAlbert Wang <example@gmail.com>\n'
        self.check_extract_username_from_shortlog(
            shortlog,
            'example@gmail.com',
            3,
        )

    def test_gets_uber_emails(self):
        shortlog = '     3\tAlbert Wang <albertyw@uber.com>\n'
        self.check_extract_username_from_shortlog(shortlog, 'albertyw', 3)

    def test_gets_user_weight(self):
        shortlog = '     2\tAlbert Wang <albertyw@uber.com>\n'
        self.check_extract_username_from_shortlog(shortlog, 'albertyw', 2)

    def test_get_changed_files(self):
        with self.assertRaises(NotImplementedError):
            self.finder.get_changed_files()

    @patch('subprocess.run')
    def test_gets_reviewers(self, mock_run):
        changed_files = ['README.rst']
        self.finder.get_changed_files = MagicMock(return_value=changed_files)
        process = MagicMock()
        git_shortlog = b'     3\tAlbert Wang <albertyw@uber.com>\n'
        git_shortlog += b'3\tAlbert Wang <example@gmail.com>\n'
        process.stdout = git_shortlog
        mock_run.return_value = process
        users = self.finder.get_reviewers()
        reviewers = Counter({'albertyw': 3, 'example@gmail.com': 3})
        self.assertEqual(users, reviewers)


class TestLogReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindLogReviewers(reviewers.Config())

    def test_get_changed_files(self):
        changed_files = ['README.rst', 'setup.py']
        self.finder.run_command = MagicMock(return_value=changed_files)
        files = self.finder.get_changed_files()
        self.assertEqual(files, ['README.rst', 'setup.py'])


class TestHistoricalReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindHistoricalReviewers(reviewers.Config())

    def test_get_reviewers(self):
        counter = Counter()  # type: typing.Counter[str]
        mock_get_log_reviewers = MagicMock(return_value=counter)
        self.finder.get_log_reviewers_from_file = mock_get_log_reviewers
        reviewers = self.finder.get_reviewers()
        self.assertEqual(counter, reviewers)


class TestFindArcCommitReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindArcCommitReviewers(reviewers.Config())

    def test_no_reviewers(self):
        log = ['asdf']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file(['file'])
        self.assertEqual(reviewers, Counter())

    def test_reviewers(self):
        log = ['asdf', ' Reviewed By: asdf, qwer']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file(['file'])
        self.assertEqual(reviewers, Counter({'asdf': 1, 'qwer': 1}))

    def test_multiple_reviews(self):
        log = ['asdf', ' Reviewed By: asdf, qwer', 'Reviewed By: asdf']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file(['file'])
        self.assertEqual(reviewers, Counter({'asdf': 2, 'qwer': 1}))


class TestShowReviewers(unittest.TestCase):
    @patch('builtins.print')
    def test_show_reviewers(self, mock_print):
        usernames = ['asdf', 'albertyw']
        reviewers.show_reviewers(usernames, False)
        mock_print.assert_called_with('asdf, albertyw')

    @patch('subprocess.Popen')
    def test_copy_reviewers(self, mock_popen):
        usernames = Counter({'albertyw': 1, 'asdf': 2})
        reviewers.show_reviewers(usernames, True)
        self.assertTrue(mock_popen.called)

    @patch('subprocess.Popen')
    def test_copy_reviewers_no_pbcopy(self, mock_popen):
        usernames = Counter({'albertyw': 1, 'asdf': 2})
        mock_popen.side_effect = FileNotFoundError
        reviewers.show_reviewers(usernames, True)


class TestGetReviewers(unittest.TestCase):
    @patch('builtins.print')
    def test_verbose_reviewers(self, mock_print):
        config = reviewers.Config()
        config.verbose = True
        counter = Counter({'asdf': 1, 'qwer': 1})
        get_reviewers = (
            'git_reviewers.reviewers.'
            'FindFileLogReviewers.get_reviewers'
        )
        run_command = 'git_reviewers.reviewers.FindReviewers.run_command'
        with patch.object(sys, 'argv', ['reviewers.py', '--verbose']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(run_command) as mock_run_command:
                    with patch('subprocess.Popen') as mock_popen:
                        mock_popen().communicate.return_value = \
                                [PHAB_ACTIVATED_DATA, b'']
                        mock_run_command.return_value = []
                        mock_get_reviewers.return_value = counter
                        reviewers.get_reviewers(config)
        self.assertEqual(len(mock_print.call_args), 2)
        self.assertEqual(
            mock_print.call_args[0][0],
            'Reviewers from FindArcCommitReviewers: %s' %
            "{'asdf': 1, 'qwer': 1}"
        )


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = reviewers.Config()
        self.config_file = tempfile.NamedTemporaryFile('w')
        self.mock_args = MagicMock()
        self.mock_args.verbose = None
        self.mock_args.ignore = ''
        self.mock_args.json = ''
        self.mock_args.copy = None

    def tearDown(self):
        self.config_file.close()

    def test_default_global_json(self):
        expected_path = os.path.expanduser("~") + "/.git/reviewers"
        json_path = reviewers.Config.default_global_json()
        self.assertEqual(json_path, expected_path)

    def test_read_configs_args(self):
        self.mock_args.verbose = True
        self.config.read_configs(self.mock_args)
        self.assertTrue(self.config.verbose)
        self.assertEqual(self.config.ignores, [])
        self.assertFalse(self.config.copy)

    def test_read_configs_copy(self):
        self.mock_args.copy = True
        self.config.read_configs(self.mock_args)
        self.assertTrue(self.config.copy)

    def test_read_json(self):
        self.mock_args.ignore = 'a,b'
        self.mock_args.json = self.config_file.name
        config_file_data = {'verbose': True, 'ignore': ['c', 'd']}
        self.config_file.write(json.dumps(config_file_data))
        self.config_file.flush()
        self.config.read_configs(self.mock_args)
        self.assertTrue(self.config.verbose)
        self.assertEqual(set(self.config.ignores), set(['a', 'b', 'c', 'd']))

    def test_read_malformed_json(self):
        self.mock_args.ignore = 'a,b'
        self.mock_args.json = self.config_file.name
        self.config_file.write('')
        self.config_file.flush()
        self.config.read_configs(self.mock_args)
        self.assertEqual(set(self.config.ignores), set(['a', 'b']))

    def test_read_unusable(self):
        self.mock_args.ignore = 'a,b'
        self.mock_args.json = self.config_file.name
        self.config_file.write("[]")
        self.config_file.flush()
        self.config.read_configs(self.mock_args)
        self.assertEqual(set(self.config.ignores), set(['a', 'b']))


class TestMain(unittest.TestCase):
    @patch('builtins.print')
    def test_main(self, mock_print):
        with patch.object(sys, 'argv', ['reviewers.py']):
            reviewers.main()
        self.assertTrue(mock_print.called)

    @patch('argparse.ArgumentParser._print_message')
    def test_version(self, mock_print):
        with patch.object(sys, 'argv', ['reviewers.py', '-v']):
            with self.assertRaises(SystemExit):
                reviewers.main()
        self.assertTrue(mock_print.called)
        version = reviewers.__version__ + "\n"
        self.assertEqual(mock_print.call_args[0][0], version)

    @patch('builtins.print')
    def test_ignore_reviewers(self, mock_print):
        counter = Counter({'asdf': 1, 'qwer': 1})
        get_reviewers = (
            'git_reviewers.reviewers.'
            'FindFileLogReviewers.get_reviewers'
        )
        run_command = 'git_reviewers.reviewers.FindReviewers.run_command'
        with patch.object(sys, 'argv', ['reviewers.py', '-i', 'asdf']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(run_command) as mock_run_command:
                    with patch('subprocess.Popen') as mock_popen:
                        mock_popen().communicate.return_value = \
                            [PHAB_ACTIVATED_DATA, b'']
                        mock_run_command.return_value = []
                        mock_get_reviewers.return_value = counter
                        reviewers.main()
        self.assertEqual(mock_print.call_args[0][0], 'qwer')

    @patch('builtins.print')
    def test_phabricator_disabled_reviewers(self, mock_print):
        counter = Counter({'asdf': 1, 'qwer': 1})
        get_reviewers = (
            'git_reviewers.reviewers.'
            'FindFileLogReviewers.get_reviewers'
        )
        run_command = 'git_reviewers.reviewers.FindReviewers.run_command'
        with patch.object(sys, 'argv', ['reviewers.py']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(run_command) as mock_run_command:
                    with patch('subprocess.Popen') as mock_popen:
                        mock_popen().communicate.return_value = \
                            [PHAB_DISABLED_DATA, b'']
                        mock_run_command.return_value = []
                        mock_get_reviewers.return_value = counter
                        reviewers.main()
        self.assertEqual(mock_print.call_args[0][0], '')
