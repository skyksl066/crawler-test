import ftplib
import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ftp_upload import ensure_dir


class TestEnsureDir(unittest.TestCase):
    def test_creates_directory_when_not_exists(self):
        ftp = MagicMock()
        ensure_dir(ftp, 'crawler-test')
        ftp.mkd.assert_called_once_with('crawler-test')

    def test_ignores_error_perm_when_directory_exists(self):
        ftp = MagicMock()
        ftp.mkd.side_effect = ftplib.error_perm('550 Directory already exists')
        ensure_dir(ftp, 'crawler-test')
        ftp.mkd.assert_called_once_with('crawler-test')


if __name__ == '__main__':
    unittest.main()
