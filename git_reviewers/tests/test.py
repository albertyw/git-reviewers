from collections import Counter
import os
import json
import sys
import unittest
from unittest.mock import patch, MagicMock

from git_reviewers import reviewers

directory = os.path.dirname(os.path.realpath(__file__))
BASE_DIRECTORY = os.path.normpath(os.path.join(directory, '..', '..'))


class TestFindReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindReviewers()

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
        data = {'response': {'data': [{'fields': {'roles': ['activated']}}]}}
        data = json.dumps(data).encode("utf-8")
        mock_popen().communicate.return_value = [data, '']
        activated = self.finder.check_phabricator_activated('asdf')
        self.assertTrue(activated)

    @patch('subprocess.Popen')
    def test_check_phabricator_activated_none(self, mock_popen):
        data = {'response': {'data': []}}
        data = json.dumps(data).encode("utf-8")
        mock_popen().communicate.return_value = [data, '']
        activated = self.finder.check_phabricator_activated('asdf')
        self.assertTrue(activated)


class TestFindLogReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindFileLogReviewers()

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
        self.finder = reviewers.FindLogReviewers()

    def test_get_changed_files(self):
        changed_files = ['README.rst', 'setup.py']
        self.finder.run_command = MagicMock(return_value=changed_files)
        files = self.finder.get_changed_files()
        self.assertEqual(files, ['README.rst', 'setup.py'])

    @patch('git_reviewers.reviewers.FindHistoricalReviewers')
    @patch('subprocess.run')
    def test_no_diffs(self, mock_run, mock_historical):
        process = MagicMock()
        process.stdout = b''
        mock_run.return_value = process
        mock_historical().get_changed_files.return_value = ['asdf']
        files = self.finder.get_changed_files()
        self.assertEqual(files, ['asdf'])


class TestHistoricalReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindHistoricalReviewers()

    def test_get_changed_files(self):
        changed_files = ['README.rst', 'setup.py']
        self.finder.run_command = MagicMock(return_value=changed_files)
        files = self.finder.get_changed_files()
        self.assertEqual(files, ['README.rst', 'setup.py'])


class TestFindArcCommitReviewers(unittest.TestCase):
    def setUp(self):
        self.finder = reviewers.FindArcCommitReviewers()

    def test_no_reviewers(self):
        log = ['asdf']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file('file')
        self.assertEqual(reviewers, Counter())

    def test_reviewers(self):
        log = ['asdf', ' Reviewed By: asdf, qwer']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file('file')
        self.assertEqual(reviewers, Counter({'asdf': 1, 'qwer': 1}))

    def test_multiple_reviews(self):
        log = ['asdf', ' Reviewed By: asdf, qwer', 'Reviewed By: asdf']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file('file')
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
        counter = Counter({'asdf': 1, 'qwer': 1})
        get_reviewers = (
            'git_reviewers.reviewers.'
            'FindFileLogReviewers.get_reviewers'
        )
        phabricator_activated = (
            'git_reviewers.reviewers.'
            'FindArcCommitReviewers.check_phabricator_activated'
        )
        with patch.object(sys, 'argv', ['reviewers.py', '--verbose']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(phabricator_activated) as mock_phab:
                    mock_phab.return_value = True
                    mock_get_reviewers.return_value = counter
                    reviewers.get_reviewers('', True)
        self.assertEqual(len(mock_print.call_args), 2)
        self.assertEqual(
            mock_print.call_args[0][0],
            'Reviewers from FindArcCommitReviewers: %s' %
            "{'asdf': 1, 'qwer': 1}"
        )


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
        phabricator_activated = (
            'git_reviewers.reviewers.'
            'FindArcCommitReviewers.check_phabricator_activated'
        )
        with patch.object(sys, 'argv', ['reviewers.py', '-i', 'asdf']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(phabricator_activated) as mock_phab:
                    mock_phab.return_value = True
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
        phabricator_activated = (
            'git_reviewers.reviewers.'
            'FindArcCommitReviewers.check_phabricator_activated'
        )
        with patch.object(sys, 'argv', ['reviewers.py']):
            with patch(get_reviewers) as mock_get_reviewers:
                with patch(phabricator_activated) as mock_phab:
                    mock_phab.return_value = False
                    mock_get_reviewers.return_value = counter
                    reviewers.main()
        self.assertEqual(mock_print.call_args[0][0], '')
