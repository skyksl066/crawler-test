import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCrawlerOutputPath(unittest.TestCase):
    def test_output_written_to_output_subdir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            os.makedirs('output', exist_ok=True)
            try:
                import crawler
                with patch('requests.get') as mock_get:
                    mock_get.return_value.status_code = 200
                    crawler.main()
                self.assertTrue(
                    os.path.exists('output/crawler_output.txt'),
                    "output/crawler_output.txt should exist"
                )
                self.assertFalse(
                    os.path.exists('crawler_output.txt'),
                    "crawler_output.txt should NOT exist in root"
                )
                self.assertGreater(
                    os.path.getsize('output/crawler_output.txt'), 0,
                    "output file should not be empty"
                )
            finally:
                os.chdir(original_dir)


if __name__ == '__main__':
    unittest.main()
