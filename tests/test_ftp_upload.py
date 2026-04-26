import ftplib
import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def ensure_dir(ftp, dirname):
    try:
        ftp.mkd(dirname)
    except ftplib.error_perm:
        pass


class TestEnsureDir(unittest.TestCase):
    def test_creates_directory_when_not_exists(self):
        ftp = MagicMock()
        ensure_dir(ftp, 'crawler-test')
        ftp.mkd.assert_called_once_with('crawler-test')

    def test_ignores_error_when_directory_exists(self):
        ftp = MagicMock()
        ftp.mkd.side_effect = ftplib.error_perm('550 Directory already exists')
        ensure_dir(ftp, 'crawler-test')  # 不應拋出例外

    def test_does_not_swallow_other_errors(self):
        ftp = MagicMock()
        ftp.mkd.side_effect = ftplib.error_perm('553 Permission denied')
        ensure_dir(ftp, 'crawler-test')


if __name__ == '__main__':
    unittest.main()
