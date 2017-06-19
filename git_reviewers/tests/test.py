import os
import unittest
from unittest.mock import patch, MagicMock

from git_reviewers import reviewers

directory = os.path.dirname(os.path.realpath(__file__))
BASE_DIRECTORY = os.path.normpath(os.path.join(directory, '..', '..'))


class TestExtractUsername(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = True

    def test_gets_emails(self):
        reviewers.UBER = False
        shortlog = '     3\tAlbert Wang <a@example.com>\n'
        email = reviewers.extract_username(shortlog)
        self.assertEqual(email, 'a@example.com')

    def test_excludes_non_uber_emails(self):
        shortlog = '     3\tAlbert Wang <a@example.com>\n'
        email = reviewers.extract_username(shortlog)
        self.assertEqual(email, None)

    def test_gets_uber_emails(self):
        shortlog = '     3\tAlbert Wang <albertyw@uber.com>\n'
        email = reviewers.extract_username(shortlog)
        self.assertEqual(email, 'albertyw')


class TestGetReviewers(unittest.TestCase):
    @patch('subprocess.run')
    def test_gets_reviewers(self, mock_run):
        process = MagicMock()
        git_shortlog = b'     3\tAlbert Wang <albertyw@uber.com>\n'
        git_shortlog += b'3\tAlbert Wang <a@example.com>\n'
        process.stdout = git_shortlog
        mock_run.return_value = process
        users = reviewers.get_reviewers()
        self.assertEqual(users, ['albertyw'])


class TestShowReviewers(unittest.TestCase):
    @patch('builtins.print')
    def test_show_reviewers(self, mock_print):
        reviewers.show_reviewers(['albertyw', 'asdf'])
        mock_print.assert_called_with('albertyw, asdf')


class TestMain(unittest.TestCase):
    @patch('builtins.print')
    @patch('argparse.ArgumentParser')
    def test_main(self, mock_argparse, mock_print):
        reviewers.main()
        self.assertTrue(mock_print.called)
