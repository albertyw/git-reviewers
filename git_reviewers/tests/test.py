import os
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


class TestFindDiffLogReviewers(unittest.TestCase):
    def setUp(self):
        reviewers.UBER = False
        self.finder = reviewers.FindDiffLogReviewers()

    @patch('subprocess.run')
    def test_gets_diff_files(self, mock_run):
        process = MagicMock()
        output = b':100644 100644 f1a6032222525ced9d1db7aa87f7956948f9ef98 '
        output += b'0000000000000000000000000000000000000000 M\tREADME.rst\n'
        output += b':100755 100755 02fbb893bcd9c7f3adfe36b48de0113336a1b209 '
        output += b'0000000000000000000000000000000000000000 M\t'
        output += b'git_reviewers/reviewers.py'
        process.stdout = output
        mock_run.return_value = process
        diff_files = self.finder.get_changed_files()
        expected = ['README.rst', 'git_reviewers/reviewers.py']
        self.assertEqual(diff_files, expected)

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
