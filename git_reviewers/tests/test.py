import os
import unittest
from unittest.mock import patch, MagicMock

from git_reviewers import reviewers

directory = os.path.dirname(os.path.realpath(__file__))
BASE_DIRECTORY = os.path.normpath(os.path.join(directory, '..', '..'))


class TestFindReviewers(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = False
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

    def test_extract_username_from_email(self):
        email = 'asdf@asdf.com'
        user = self.finder.extract_username_from_email(email)
        self.assertEqual(user, email)

    def test_extract_uber_username_from_email(self):
        reviewers.UBER = True
        email = 'asdf@asdf.com'
        user = self.finder.extract_username_from_email(email)
        self.assertEqual(user, None)
        email = 'asdf@uber.com'
        user = self.finder.extract_username_from_email(email)
        self.assertEqual(user, 'asdf')


class TestFindLogReviewers(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = False
        self.finder = reviewers.FindFileLogReviewers()

    def test_gets_emails(self):
        shortlog = '     3\tAlbert Wang <a@example.com>\n'
        email = self.finder.extract_username_from_shortlog(shortlog)
        self.assertEqual(email, 'a@example.com')

    def test_excludes_non_uber_emails(self):
        reviewers.UBER = True
        shortlog = '     3\tAlbert Wang <a@example.com>\n'
        email = self.finder.extract_username_from_shortlog(shortlog)
        self.assertEqual(email, None)

    def test_gets_uber_emails(self):
        reviewers.UBER = True
        shortlog = '     3\tAlbert Wang <albertyw@uber.com>\n'
        email = self.finder.extract_username_from_shortlog(shortlog)
        self.assertEqual(email, 'albertyw')

    def test_get_changed_files(self):
        with self.assertRaises(NotImplementedError):
            self.finder.get_changed_files()

    @patch('subprocess.run')
    def test_gets_reviewers(self, mock_run):
        reviewers.UBER = True
        changed_files = ['README.rst']
        self.finder.get_changed_files = MagicMock(return_value=changed_files)
        process = MagicMock()
        git_shortlog = b'     3\tAlbert Wang <albertyw@uber.com>\n'
        git_shortlog += b'3\tAlbert Wang <a@example.com>\n'
        process.stdout = git_shortlog
        mock_run.return_value = process
        users = self.finder.get_reviewers()
        self.assertEqual(users, set(['albertyw']))


class TestFindDiffLogReviewers(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = False
        self.finder = reviewers.FindDiffLogReviewers()

    @patch('subprocess.run')
    def test_gets_diff_files(self, mock_run):
        process = MagicMock()
        output = b'README.rst\ngit_reviewers/reviewers.py\n'
        process.stdout = output
        mock_run.return_value = process
        diff_files = self.finder.get_changed_files()
        expected = ['README.rst', 'git_reviewers/reviewers.py']
        self.assertEqual(diff_files, expected)


class TestLogReviewers(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = False
        self.finder = reviewers.FindLogReviewers()

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
        self.assertEqual(reviewers, [])

    def test_reviewers(self):
        log = ['asdf', ' Reviewed By: asdf, qwer']
        self.finder.run_command = MagicMock(return_value=log)
        reviewers = self.finder.get_log_reviewers_from_file('file')
        self.assertEqual(reviewers, ['asdf', 'qwer'])


class TestShowReviewers(unittest.TestCase):
    @patch('builtins.print')
    def test_show_reviewers(self, mock_print):
        reviewers.show_reviewers(['albertyw', 'asdf'])
        mock_print.assert_called_with('albertyw, asdf')


class TestMain(unittest.TestCase):
    @patch('builtins.print')
    @patch('argparse.ArgumentParser')
    def test_main(self, mock_argparse, mock_print):
        mock_argparse().parse_args().path = ""
        reviewers.main()
        self.assertTrue(mock_print.called)
